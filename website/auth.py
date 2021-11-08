from flask import Blueprint,render_template,request,flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

    return render_template('login.html')

@auth.route('/logout')
def login():
    return '<p>logout</p>'

@auth.route('/sign-up')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if user:
            flash('Email already exists', category='error')

        if len(email) < 4 :
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2 :
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 5:
            flash('Passowrd must be atleast 5 characters', category='error')


    return render_template('sign_up.html')