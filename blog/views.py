from flask import Blueprint, render_template
from sqlalchemy import desc
from flask_login import login_required, current_user
import copy
from app import db
from blog.forms import PostForm
from models import Post, User

blog_blueprint = Blueprint('blog', __name__, template_folder='templates')

#user = User.query.first()
#postkey = user.postkey

@blog_blueprint.route('/blog')
@login_required
def blog():
    posts = Post.query.order_by(desc('id')).all()

    # creates a list of copied post objects which are independent of database.
    post_copies = list(map(lambda x: copy.deepcopy(x), posts))

    # empty list for decrypted copied post objects
    decrypted_posts = []

    # decrypt each copied post object and add it to decrypted_posts array.
    for p in post_copies:
        user = User.query.filter_by(username=p.username).first()
        p.view_post(user.postkey)
        decrypted_posts.append(p)

    return render_template('blog.html', posts=decrypted_posts)

@blog_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(username=current_user.username, title=form.title.data, body=form.body.data, postkey=current_user.postkey)

        db.session.add(new_post)
        db.session.commit()

        return blog()
    return render_template('create.html', form=form)

@blog_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return render_template('500.html')

    form = PostForm()

    if form.validate_on_submit():
        post.update_post(form.title.data, form.body.data, current_user.postkey)
        return blog()

    # creates a copy of post object which is independent of database.
    post_copy = copy.deepcopy(post)

    # decrypt copy of post object.
    post_copy.view_post(current_user.postkey)

    # set update form with title and body of copied post object
    form.title.data = post_copy.title
    form.body.data = post_copy.body

    return render_template('update.html', form=form)
@blog_blueprint.route('/<int:id>/delete')
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return blog()
