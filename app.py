"""Blogly application."""

from flask import Flask, request, flash
from flask.templating import render_template
from werkzeug.utils import redirect
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
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


###############################################
@app.route("/")
def home():
    """Home page"""

    lastPosts = Post.query.order_by(Post.id.desc()).limit(5).all()

    return render_template("home.html", posts=lastPosts)


@app.route("/users")
def users_list():
    """Show list of users"""

    users = User.query.order_by(User.last_name).all()

    return render_template("userListing.html", users=users)


@app.route("/users/new", methods=['GET'])
def new_user_form():
    """show form to create new user"""

    return render_template("createUser.html")


@app.route("/users/new", methods=['POST'])
def new_user():
    """Create new user and add it to db"""

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
    """show user details"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template("details.html", user=user, posts=posts)


@app.route('/users/<user_id>/edit', methods=['GET'])
def edit_user_form(user_id):
    """Shhow form to edit user"""

    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)


@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


###############################################
@app.route("/users/<user_id>/posts/new", methods=['GET'])
def new_post_form(user_id):
    """Show form to add post for a given user"""

    user = User.query.get_or_404(user_id)

    return render_template("createPost.html", user=user)


@app.route("/users/<user_id>/posts/new", methods=['POST'])
def new_post(user_id):
    """Create new post and add it to db"""

    title = request.form['title']
    content = request.form['content']

    if not (title and content):
        flash("Complete all fields before submitting!")

        return redirect(f"/users/{user_id}/posts/new")

    else:
        post = Post(
            title=title,
            content=content,
            user_id=user_id
        )

        db.session.add(post)
        db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<post_id>')
def post_page(post_id):
    """show post details"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("postDetails.html", user=user, post=post)


@app.route('/posts/<post_id>/edit', methods=['GET'])
def edit_post_form(post_id):
    """Show form to edit a post"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("editPost.html", post=post, user=user)


@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edit user"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


###############################################
@app.route('/tags')
def tags_index():
    """info on all tags"""

    tags = Tag.query.all()
    return render_template('tagList.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show page to create a new tag"""

    posts = Post.query.all()
    return render_template('createTag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle creation of a new tag"""

    post_ids = [int(num) for num in request.form.getlist(
        "posts")]  # num is a string in DOM
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('editTag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
