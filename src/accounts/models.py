from datetime import datetime
from cryptography.fernet import Fernet
from flask_login import UserMixin
from src import bcrypt, db
from sqlalchemy.dialects.postgresql import ARRAY

# Table that holds all user data
class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<email {self.email}>"


# Table that holds all event data
class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False, default=False)
    body  = db.Column(db.Text, nullable=False, default=False)
    location = db.Column(db.String, nullable=False, default=False) # Serialize floats into string
    likes = db.Column(db.Integer, default = 0) # How many likes the event has
    inviteonly = db.Column(db.Boolean, default= False) # make an event invite only


    def __init__(self, creator_id, title, body, location):
        self.creator_id = creator_id
        self.created = datetime.now()
        self.title = title
        self.body = body
        self.location = location

    def update_event(self, title, body):
        self.title = title
        self.body = body
        db.session.commit()

    def view_event(self):
        self.title = self.title
        self.body = self.body

# Table that link events and users that participate in the event
class Participate(db.Model):
    __tablename__ = 'participate'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    event_id = db.Column(db.String, db.ForeignKey(Event.id), nullable=False)

# Table that links events and users, users can save an event
class LikedEvent(db.Model):
    __tablename__ = 'likedevent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    event_id = db.Column(db.String, db.ForeignKey(Event.id), nullable=False)

# Table that links events and users that request to participate to an event
class WantToParticipate(db.Model):
    __tablename__ = 'wanttoparticipate'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    event_id = db.Column(db.String, db.ForeignKey(Event.id), nullable=False)