"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


def connect_db(app):
    """Connect this database to provided Flask app.
    To be call in app file
    """

    db.app = app
    db.init_app(app)
