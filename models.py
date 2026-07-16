from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Creating the db in Flask. variables represent how it would be done in SQL
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60),unique=True,nullable=False)

    #Stores hash, not the real password
    password = db.Column(db.String(255),nullable=False)