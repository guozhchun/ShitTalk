from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from Model import Post
from werkzeug.contrib.fixers import ProxyFix
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

# <<<<<<< HEAD
# app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
   #app.run(debug=True, port = 8080, host='192.168.1.238')
   app.run(debug = True)
# =======

# if __name__ == '__main__':
#     app.run(debug=True, port=80, host='192.168.1.103')
# >>>>>>> 7094cbaf654b6a7506ba89bc10042c05ce052343

#     