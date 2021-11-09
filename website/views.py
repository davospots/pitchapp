
from flask import Blueprint,render_template,flash,request,jsonify,redirect,url_for
from flask.json import jsonify
from flask_login import login_required,current_user

from website.auth import login
from .models import Post,User
from . import db
import json

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

    pitches = Post.query.filter_by(author=user.id).all()

    return render_template('pitches.html',user=current_user,pitches=pitches,username=username)