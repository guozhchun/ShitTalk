from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap
from Model import Post, db
from werkzeug.contrib.fixers import ProxyFix
from celery import Celery
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
bootstrap = Bootstrap(app)
db.app = app
db.init_app(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# celery operation in background
@celery.task
def addTalk(cont, locat):
	newPost = Post(content=cont, location=locat)
	db.session.add(newPost)
	db.session.commit()
	print Post.query.all()

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['post_content'] != "":
			cont = request.form['post_content']
			locat = 0
			addTalk.delay(cont, locat)
		
	return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == 'POST':
		print request.form['test']
	return render_template('main.html')


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
