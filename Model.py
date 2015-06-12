from flask.ext.sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	like_num = db.Column(db.Integer, default = 0)
	create_time = db.Column(db.DateTime, default=datetime.datetime.now)
	location = db.Column(db.Integer)

	comment_id = db.relationship('PostComment', backref='post')

	def __repr__(self):
		return '<Post %s>' % self.content


class PostComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text)
	create_time = db.Column(db.DateTime, default=datetime.datetime.now)
	
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

	def __repr__(self):
		return '<Comment %s>' % self.content
