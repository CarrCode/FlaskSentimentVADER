from datetime import datetime
from app import db

class Post(db.Model):
    body = db.Column(db.String(200), primary_key=True)
    sentiment = db.Column(db.String(30))