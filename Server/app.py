import sys

sys.path.append('/workspace/framework_spider/')
from flask import Flask

from Server.bluePrint.pc.index import index_bp
from Server.bluePrint.pc.single import single_bp
from Server.bluePrint.pc.lists import list_bp
from Server.bluePrint.pc.news_single import news_single_bp
from Server.bluePrint.pc.news_lists import news_list_bp
from Server.bluePrint.weixin.wechat import weChat_bp

app = Flask(__name__,static_folder='templates',static_url_path='/')

app.register_blueprint(index_bp)
app.register_blueprint(single_bp)
app.register_blueprint(list_bp)
app.register_blueprint(news_single_bp)
app.register_blueprint(news_list_bp)
app.register_blueprint(weChat_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8086)