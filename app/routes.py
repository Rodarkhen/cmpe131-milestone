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

# Route for the home page
@myapp_obj.route('/home')
@login_required
def home():
    user_notes = current_user.notes.all()  # Fetch all notes for the current user
    return render_template('home.html', name=current_user.name, user_notes=user_notes)

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
        return redirect(url_for('login'))
    
    # Check if the username and email is already taken
    username_error = form.validate_username(form.username)
    email_error = form.validate_email(form.email)

    # Check if the passwords match
    if form.password.data != form.confirm.data:
        password_error = "Password mismatch"
    
    # Render the sign-up form template with any validation messages
    return render_template('sign_up.html', form=form, username_error=username_error, email_error=email_error, password_error=password_error)

@myapp_obj.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out.', 'success')
    return redirect(url_for('home'))

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

@myapp_obj.route('/create_note', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()

    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(note)
        db.session.commit()

        flash('Note created successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('create_note.html', form=form)

@myapp_obj.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if the current user is the owner of the note
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', 'error')
        return redirect(url_for('home'))

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()

        flash('Note updated successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('edit_note.html', form=form, note=note)

@myapp_obj.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if the current user has permission to delete the note
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note.', 'error')
        return redirect(url_for('home'))

    db.session.delete(note)
    db.session.commit()

    flash('Note deleted successfully.', 'success')
    return redirect(url_for('home'))

@myapp_obj.route('/search_notes', methods=['GET', 'POST'])
@login_required
def search_notes():
    form = SearchForm()

    if form.validate_on_submit():
        search_query = form.search_query.data
        # Perform the search based on your criteria
        user_notes = current_user.notes.filter(
            (Note.title.contains(search_query)) | (Note.content.contains(search_query))).all()

        return render_template('search_notes.html', form=form, user_notes=user_notes)

    return render_template('search_notes.html', form=form, user_notes=None)