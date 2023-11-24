# routes.py
from markupsafe import escape
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app import myapp_obj, db
from app.models import User
from .forms import SignUpForm, LoginForm, EditProfileForm
from datetime import datetime

@myapp_obj.route('/')
@myapp_obj.route('/home')
def home():
    return render_template(url_for('base'))

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

        # Add to the database
        db.session.add(u)
        db.session.commit()

        # Flash a success message and redirect to the home page
        flash('Account created successfully.', 'success')
        return redirect(url_for('home'))
    
    # Check if the username and email is already taken
    username_error = form.validate_username(form.username)
    email_error = form.validate_email(form.email)

    # Check if the passwords match
    if form.password.data != form.confirm.data:
        password_error = "Password mismatch"
    
    # Render the sign-up form template with any validation messages
    return render_template('sign_up.html', form=form, username_error=username_error, email_error=email_error, password_error=password_error)

@myapp_obj.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    # Initialize error messages
    username_error = None
    email_error = None

    if form.validate_on_submit():
        # Check if the username and email is already taken
        if  form.exist_username(form.username) and form.username.data != current_user.username:
            username_error = 'Username already taken'
        if  form.exist_email(form.email) and form.email.data != current_user.email:
            email_error = 'Email already taken.'
        # If either the username or email is taken, display an error message
        if username_error or email_error:
            return render_template('edit_profile.html', form=form, username_error=username_error, email_error=email_error)
        # Updates the current user information
        current_user.update_info(form.name.data, form.username.data, form.email.data)
        flash('Changes Saved!.', 'success')
        return redirect(url_for('home'))
    
    # Pre-fill the form with the current user information
    form.name.data = current_user.name
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.created_at.data = current_user.created_at.strftime("%m-%d-%Y")  # Convert datetime to string for display

    return render_template('edit_profile.html', form=form)

@myapp_obj.route('/create_note')
def create_note():
    return render_template('create_note.html')
# Add more routes as needed

