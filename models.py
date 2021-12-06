"""Models for Blogly."""

from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.
    To be call in app file
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)

    # @property makes the method usable like an attribute
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Handle relationship between the two models, and cascading deletion
    user = relationship("User", backref=backref(
        "post", cascade="all, delete-orphan"))

    # Through relationship
    tags = relationship("Tag", secondary="postTags", backref="posts")


class Tag(db.Model):
    """Tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)


class PostTag(db.Model):
    """PostTag model"""

    __tablename__ = "postTags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
