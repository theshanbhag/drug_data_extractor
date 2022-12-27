from flask import Flask, render_template, request
import pymongo
import configparser
from google.cloud import vision


parser = configparser.ConfigParser()
parser.read("config.txt")
app = Flask(__name__)

myclient = pymongo.MongoClient(parser.get("config", "uri"), tlsAllowInvalidCertificates=True)
mydb = myclient["AppEngineTest"]
mycol = mydb["Employee"]
client = vision.ImageAnnotatorClient()



@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/submit", methods=['GET'])
def docs():
    args = request.args
    file_path = args['Bucket path']
    blob_source = vision.Image(source=vision.ImageSource(image_uri=file_path))
    results = client.text_detection(image=blob_source)
    print(results)
    print(">>>>>>>>>>>>>")
    return "Done"


@app.route("/find", methods=['GET'])
def find():
    args = request.args
    print("Hello World !!!!!")
    x = mycol.find_one({"Name": args["find"]})
    print(x.values())

    return render_template("find.html", Names=x.items())


if __name__ == "__main__":
    app.run(debug=True)
