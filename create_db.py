from Model import db
from ShitTalk import app



db.app(app)
db.init_app(app)
db.create_all()
