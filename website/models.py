from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64))
    password = db.Column(db.String(32))
    notes = db.relationship('Note')
    posts = db.relationship('Post')
    likes = db.relationship('Like')
    comments = db.relationship('Comment')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    link = db.Column(db.String(256))
    author = db.Column(db.String(256))
    image = db.Column(db.String(256))
    content = db.Column(db.String(10000))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    content = db.Column(db.String(3000))
    likes = db.relationship('Like')
    comments = db.relationship('Comment')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(300))


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Following(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True);
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True);

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now)

