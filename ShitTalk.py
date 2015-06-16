from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap
from Model import Post, db, PostComment
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
	with app.app_context():
		newPost = Post(content=cont, location=locat)
		db.session.add(newPost)
		db.session.commit()
		print Post.query.all()

@celery.task
def addComment(cont, locat):
	with app.app_context():
		newCom = PostComment(content=comt, post_id = post_id)
		db.session.add(newCom)
		db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['post_content'] != "":
			cont = request.form['post_content']
			locat = 0
			addTalk.delay(cont, locat)

	post = Post.query.all()
	post_id = []
	post_contents = []
	for x in post:
		post_id.append(str(x.id))
		post_contents.append(x.content)
	length = len(post)
	return render_template('index.html', post_id = post_id, post_contents = post_contents, length = length)

@app.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == 'POST':
		print request.form['test']
	return render_template('main.html')


@app.route('/comment/<post_id>', methods=['GET', 'POST'])
def comment(post_id):
	post = Post.query.filter_by(id = int(post_id)).first()

	if post != None:
		if request.method == 'POST':
			if request.form['comment_content'] != "":
				comt = request.form['comment_content']
				post_id = post.id
				addComment.delay(comt, post_id)

		post_content = post.content
		post_like = post.like_num
		post_time = post.create_time
		comments = PostComment.query.filter_by(id = int(post_id)).all()
		coms = []
		coms_time = []
		if comments != []:
			for x in comments:
				coms.append(x.content)
				coms_time.append(x.create_time)
		length = len(comments)
		return render_template('comment.html', length = length, comments = coms, comments_time = coms_time, post_content = post_content, post_time = post_time, post_like = post_like, post_id = post_id)
	return rendirect(url_for('/'))



# <<<<<<< HEAD
# app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	#app.run(debug=True, port = 8080, host='192.168.1.238')
    app.run(debug = True)
# # =======

# if __name__ == '__main__':
#     app.run(debug=True, port=8090, host='192.168.1.102')
# >>>>>>> 7094cbaf654b6a7506ba89bc10042c05ce052343

#     
