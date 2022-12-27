from flask import Flask, render_template, request, redirect
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse
import json
import pymongo
import configparser

parser = configparser.ConfigParser()
parser.read("config.txt")
app = Flask(__name__)

mongo_client = pymongo.MongoClient(parser.get("config", "uri"), tlsAllowInvalidCertificates=True)
mydb = mongo_client[parser.get("config", "database")]
mycol = mydb[parser.get("config", "collection")]
vision_client = vision.ImageAnnotatorClient()


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/submit", methods=['GET'])
def docs():
    # get file path from frontend
    args = request.args
    file_path = args['Bucket path']

    # extract data using Google vision API
    blob_source = vision.Image(source=vision.ImageSource(image_uri=file_path))
    results = vision_client.text_detection(image=blob_source)

    # Serialize the data and convert to json format
    serialized_proto_plus = AnnotateImageResponse.serialize(results)
    response = AnnotateImageResponse.deserialize(serialized_proto_plus)
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)

    try:
        mycol.insert_one(response)
    except Exception as e:
        print(e)
        return "Exception occurred :" + str(e)
    return render_template("success.html")


@app.route("/find", methods=['GET'])
def find():
    args = request.args
    print("Hello World !!!!!")
    x = mycol.find_one({"Name": args["find"]})
    print(x.values())

    return render_template("find.html", Names=x.items())


if __name__ == "__main__":
    app.run(debug=True)
