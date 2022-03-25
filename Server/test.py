# coding:utf-8
from flask import Flask,request,jsonify

app = Flask(__name__)


@app.route('/getMedia')
def getMedia():
    return jsonify([
        {"siteName":"傲立机床网"},
        {"siteName":"JC35机床网"}
    ])


app.run(
    host="0.0.0.0",port=8086
)