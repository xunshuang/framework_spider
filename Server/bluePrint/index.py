from flask import Flask, Blueprint, request,jsonify,render_template

from Db.MySQLClient.client import create_new_mysql
from Config.GlobalSetting import MYSQL_CONFIG

index_bp = Blueprint('index', __name__)


# 首页
@index_bp.route('/')
def index():
    return render_template("index.html")

