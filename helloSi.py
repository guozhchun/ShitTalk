# I
# G
# N
# O
# R
# E
#
# T
# H
# I
# S
#
# I
# D
# I
# O
# T

from flask import Flask, render_template, request, jsonify, redirect, url_for
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

@celery.task
def addComment(comt, post_id):
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
			return redirect(url_for('index'))

	post = Post.query.all()
	post_id = []
	post_contents = []
	post_like = []
	comment_num = []
	# for x in post:
	# 	post_id.append(str(x.id))
	# 	post_contents.append(x.content)
	# 	post_like.append(x.like_num)
	# 	comment_num.append(len(PostComment.query.filter_by(post_id = int(x.id)).all()))
	for x in range(0,len(post))[::-1]:
		post_id.append(str(post[x].id))
		post_contents.append(post[x].content)
		post_like.append(post[x].like_num)
		comment_num.append(len(PostComment.query.filter_by(post_id = int(post[x].id)).all()))
	length = len(post)
	return render_template('index.html', post_id = post_id, comment_num = comment_num, post_like = post_like, post_contents = post_contents, length = length)

@app.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == 'POST':
		print request.form['test']
	return render_template('main.html')


# o
# l
# a
# l
# a
# l
# a
# l
# a
# l
# a

@app.route('/comment/<post_id>', methods=['GET', 'POST'])
def comment(post_id):
	post = Post.query.filter_by(id = int(post_id)).first()

	if post != None:
		if request.method == 'POST':
			if request.form['comment_content'] != "":
				comt = request.form['comment_content']
				post_id = post.id
				addComment.delay(comt, post_id)
				# addComment(comt,post_id)
				return redirect(url_for('comment', post_id = post_id))
		post = Post.query.filter_by(id = int(post_id)).first()
		post_content = post.content
		post_like = post.like_num
		post_time = post.create_time

		comments = PostComment.query.filter_by(post_id = int(post_id)).all()
		coms = []
		coms_time = []
		if comments != []:
			for x in comments:
				coms.append(x.content)
				coms_time.append(x.create_time)
		length = len(comments)
		post_id = str(post_id)
		return render_template('comment.html', length = length, comments = coms, comments_time = coms_time, post_content = post_content, post_time = post_time, post_like = post_like, post_id = post_id)
	return redirect(url_for('index'))

@app.route('/addLike', methods=['GET', 'POST'])
def addLike():
	if request.method == "POST":
		post_id = request.json['post_id']
		post = Post.query.filter_by(id = int(post_id)).first()
		post.like_num = post.like_num + 1
		db.session.commit()
		return jsonify(status="success")

@app.route('/removeLike', methods=['GET', 'POST'])
def removeLike():
	if request.method == "POST":
		post_id = request.json['post_id']
		post = Post.query.filter_by(id = int(post_id)).first()
		post.like_num = post.like_num - 1
		db.session.commit()
		return jsonify(status="success")


# <<<<<<< HEAD
app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
# 	#app.run(debug=True, port = 8080, host='192.168.1.238')
    app.run(debug = True)
# # =======

# if __name__ == '__main__':
    # app.run(debug=True, port=8000, host='192.168.1.102')

#     
