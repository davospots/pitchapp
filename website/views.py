
from flask import Blueprint,render_template,flash,request,jsonify,redirect,url_for

from flask_login import login_required,current_user

from website.auth import login
from .models import Post,User,Comment,Like  
from . import db


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)
    

@views.route("/delete-pitch/<id>")
@login_required
def delete_pitch(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Pitch does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this pitch.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Pitch deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/create-pitch", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Pitch cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Pitch created', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_pitch.html', user=current_user)

@views.route('/pitches/<username>')
@login_required
def pitches(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts

    return render_template('pitches.html',user=current_user,posts=posts,username=username)


@views.route('/create-comment/<post_id>', methods=['POST'])
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty', category='error')

    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Pitch does not exist',category='error')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
@login_required
def def_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-pitch/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

