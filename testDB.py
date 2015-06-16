from Model import Post, PostComment
from Model import db
from ShitTalk import app

db.app = app
db.init_app(app)

test1 = Post(content="test5", location=0)
db.session.add(test1)

allPost = Post.query.all()
for x in allPost:
	print x.like_num

