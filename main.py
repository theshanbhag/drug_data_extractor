from flask import Flask, render_template, request, redirect
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse
from google.cloud import storage
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
    bucket_name = args['Bucket name']
    folder_name = args['Folder name']
    storage_client = storage.Client()
    bucket = storage.Bucket(storage_client, bucket_name)
    try:
        blobs = bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            print(blob.name)
            blob_source = vision.Image(
                source=vision.ImageSource(image_uri="gs://" + str(bucket_name) + "/" +str(blob.name)))
            results = vision_client.text_detection(image=blob_source)
            serialized_proto_plus = AnnotateImageResponse.serialize(results)
            response = AnnotateImageResponse.deserialize(serialized_proto_plus)
            response_json = AnnotateImageResponse.to_json(response)
            response = json.loads(response_json)
            try:
                mycol.insert_one(response["fullTextAnnotation"])
            except Exception as e:
                print(e)
    except Exception as e:
        print(str(e))

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
