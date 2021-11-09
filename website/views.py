
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
    notes = Post.query.all()
    return render_template ('home.html', user=current_user, notes=notes)
    

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/create-post", methods=['GET', 'POST'])
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

    return render_template('create_post.html', user=current_user)

