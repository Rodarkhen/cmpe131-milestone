# routes.py
from markupsafe import escape
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app import myapp_obj, db
from .models import User, Note
from .forms import SignUpForm, LoginForm, EditProfileForm, NoteForm, SearchForm
from datetime import datetime

@myapp_obj.route('/')
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to home page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
        # Redirect to the page the user intended to visit before login (if available),
        # or redirect to the home page
        next_page = request.args.get('next') or url_for('home')
    return render_template('login.html', form=form)

@myapp_obj.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out.', 'success')
    return redirect(url_for('home'))

# Route for handling user sign-up
@myapp_obj.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    # Initialize error messages
    username_error = None
    email_error = None
    password_error = None

    print(form.validate_on_submit()) # debug 
    if form.validate_on_submit():
        # Create a new User instance
        u = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            created_at=datetime.now()
        )
        # Hash the password
        u.set_password(form.password.data)
        # Check if the passwords match
        if form.password.data != form.confirm.data:
            password_error = "Passwords do not match."

        # add to the database
        db.session.add(u)
        db.session.commit()

        # Flash a success message and redirect to the home page
        flash('Account created successfully. Now you can log in!', 'success')
        return redirect('/')
    
    # Check if the username is already in use
    if User.query.filter_by(username=form.username.data).first():
        username_error = "Username is already in use."
    # Check if the email is already in use
    if User.query.filter_by(email=form.email.data).first():
        email_error = "Email is already in use."
    
    # Render the sign-up form template with any validation messages
    return render_template('sign_up.html', form=form, username_error=username_error, email_error=email_error, password_error=password_error)

@myapp_obj.route('/create_note')
def create_note():
    #Get method (action) from HTML
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML
        title = request.form.get('title')  #Gets title from HTML

        #IF note data is less than 1, then display error
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
        #IF note sufficent length, then add the note to database
            new_note = Note(data=note, note_title=title)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('create_note.html')
# Add more routes as needed

