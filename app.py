"""Blogly application."""

from flask import Flask, request, flash
from flask.templating import render_template
from werkzeug.utils import redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# the toolbar is only enabled in debug mode:
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'nerea'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home():

    return redirect("/users")


@app.route("/users")
def users_list():

    users = User.query.order_by(User.last_name).all()

    return render_template("userListing.html", users=users)


@app.route("/users/new", methods=['GET'])
def new_user_form():

    return render_template("createUser.html")


@app.route("/users/new", methods=['POST'])
def new_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if not (first_name and last_name):
        flash("Complete all fields before submitting!")

        return redirect('/users/new')

    else:
        user = User(
            first_name=first_name,
            last_name=last_name,
            image_url=image_url
        )

        db.session.add(user)
        db.session.commit()

    return redirect("/users")


@app.route('/users/<user_id>')
def user_page(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("details.html", user=user)


@app.route('/users/<user_id>/edit', methods=['GET'])
def edit_user_form(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)


@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
