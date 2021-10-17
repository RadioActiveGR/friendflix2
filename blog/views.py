from flask import Blueprint, render_template
from sqlalchemy import desc
from app import db
from blog.forms import PostForm
from models import Post, User

blog_blueprint = Blueprint('blog', __name__, template_folder='templates')

user = User.query.first()
postkey = user.postkey

@blog_blueprint.route('/blog')
def blog():
    posts = Post.query.order_by(desc('id')).all()

    for p in posts:
        p.view_post(postkey)

    return render_template('blog.html', posts=posts)


@blog_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(username=None, title=form.title.data, body=form.body.data, postkey=postkey)

        db.session.add(new_post)
        db.session.commit()

        return blog()
    return render_template('create.html', form=form)

@blog_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        return render_template('500.html')

    form = PostForm()

    if form.validate_on_submit():
        Post.query.filter_by(id=id).update({"title": form.title.data})
        Post.query.filter_by(id=id).update({"body": form.body.data})

        db.session.commit()

        post.update_post(form.title.data, form.body.data, postkey)

        return blog()

    post.view_post(postkey)

    form.title.data = post.title
    form.body.data = post.body

    return render_template('update.html', form=form)

@blog_blueprint.route('/<int:id>/delete')
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return blog()
