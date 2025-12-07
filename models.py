from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(200), nullable=True)
    achievement_pdf = db.Column(db.String(200), nullable=True)
    research_pdf = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    photo = db.Column(db.String(200), nullable=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(200), nullable=True)


class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class Galleries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(200), nullable=False)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    year = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class Committee(db.Model):
    __tablename__ = 'committees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    members = db.relationship('Member', backref='committee', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Committee(id={self.id}, name={self.name}, type={self.type})>"


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Member(id={self.id}, name={self.name}, designation={self.designation})>"