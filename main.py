from flask import Flask, render_template, Request, request
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient(
        "mongodb+srv://venkatesh:ashwin123@iiotapp.2wqno.mongodb.net/?retryWrites=true&w=majority",
        tlsAllowInvalidCertificates=True)
mydb = myclient["AppEngineTest"]
mycol = mydb["Employee"]

@app.route("/")
def homepage():
    # name_list = []
    # for i in x[0:10]:
    #     name_list.append(i["_id"])
    return render_template("index.html")


@app.route("/submit", methods=['GET'])
def docs():
    args = request.args
    x = mycol.insert_one({"Name":args["fname"],"Surname":args["lname"]})
    if x.acknowledged:
        return render_template("index2.html", Names="Data Interested Successfully")
    return render_template("index2.html", Names="Data Insertion Failed !!!!!!")


@app.route("/find", methods=['GET'])
def find():
    args = request.args
    print("Hello World !!!!!")
    x = mycol.find_one({"Name":args["find"]})

    return render_template("find.html", Names=x.items())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

