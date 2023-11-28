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



