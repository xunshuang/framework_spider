from flask import Flask
import sys
import os


sys.path.append('/workspace/')
from flask import Flask

from Server.bluePrint.index import index_bp
from Server.bluePrint.single import single_bp
from Server.bluePrint.lists import list_bp

app = Flask(__name__,static_folder='templates',static_url_path='/')

app.register_blueprint(index_bp)
app.register_blueprint(single_bp)
app.register_blueprint(list_bp)
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8086)