# routes.py
from markupsafe import escape
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app import myapp_obj, db
from .models import User, Note
from .forms import SignUpForm, LoginForm, EditProfileForm, NoteForm, SearchForm
from datetime import datetime
from faker import Faker

# Route for handling user login
@myapp_obj.route('/', methods=['GET', 'POST'])
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to home page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm() # Create a login form instance

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Query the database for the user based on the entered username
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if the user exists and the provided password is correct
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            login_user(user, remember=form.remember_me.data)
            # Redirect to the home page after successful login
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
        # Redirect to the page the user intended to visit before login (if available),
        # or redirect to the home page
        next_page = request.args.get('next') or url_for('home')
    
    # Render the login template with the login form
    return render_template('login.html', form=form)


# Route for the home page
@myapp_obj.route('/home')
@login_required
def home():
    # Retrieve all notes for the current user
    user_notes = current_user.notes.all()
    # Render the home template with the user's name and notes
    return render_template('home.html', name=current_user.name, user_notes=user_notes)


# Route for handling user sign-up
@myapp_obj.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    # Create a sign-up form instance
    form = SignUpForm()

    # Initialize error messages
    username_error = None
    email_error = None
    password_error = None

    print(form.validate_on_submit()) # for debug 

    # Check if the form is submitted and valid
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
    return render_template('sign_up.html', form=form, username_error=username_error, email_error=email_error,
                           password_error=password_error)


# Route for user logout
@myapp_obj.route('/logout')
def logout():
    # Log out the user if they are authenticated
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out.', 'success') # Flash message
    # Redirect to the home page
    return redirect(url_for('home'))

# Route for editing user profile
@myapp_obj.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Create an EditProfileForm instance
    form = EditProfileForm()

    # Initialize error messages
    username_error = None
    email_error = None

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Check if the username and email is already taken
        if form.exist_username(form.username) and form.username.data != current_user.username:
            username_error = 'Username already taken'
        if form.exist_email(form.email) and form.email.data != current_user.email:
            email_error = 'Email already taken.'
        # If either the username or email is taken, display the error message
        if username_error or email_error:
            return render_template('edit_profile.html', form=form, username_error=username_error, email_error=email_error)
        # Updates the current user information and redirects to home page
        current_user.update_info(form.name.data, form.username.data, form.email.data)
        flash('Changes Saved!.', 'success')
        return redirect(url_for('home'))

    # Pre-fill the form with the current user information
    form.name.data = current_user.name
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.created_at.data = current_user.created_at.strftime("%m-%d-%Y")  # Convert datetime to string for display

    # Render the edit profile template with the form
    return render_template('edit_profile.html', form=form)


@myapp_obj.route('/create_note', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()

    # Check if the form is submitted
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,  # Set the user_id to the current user's ID (database)
            created_at=datetime.utcnow()  # Set the creation time to the current time
        )
        db.session.add(note)
        db.session.commit()  # ADD and COMMIT to save changes to database

        flash('Note created successfully.', 'success')  # Show success
        return redirect(url_for('home'))  # Redirect to home

    return render_template('create_note.html', form=form)


# Route to edit an existing note, identified by its ID
@myapp_obj.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required  # Ensures that only authenticated users can access this route
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if the current user is the owner of the note
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.', 'error')
        return redirect(url_for('home'))

    form = NoteForm(obj=note)  # FILL the form with the note's existing data

    # Update the note with new data from the form (After Validation)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()  # COMMIT changes

        flash('Note updated successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('edit_note.html', form=form, note=note)


# Route to delete a note, specified by its ID
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

# Route for searching notes
@myapp_obj.route('/search_notes', methods=['GET', 'POST'])
@login_required
def search_notes():
    form = SearchForm()

    # Handle the search logic upon form submission/validation
    if form.validate_on_submit():
        search_query = form.search_query.data
        # Perform the search based on your criteria
        user_notes = current_user.notes.filter(
            (Note.title.contains(search_query)) | (Note.content.contains(search_query))).all()

        # Render the search results page with the form and notes
        return render_template('search_notes.html', form=form, user_notes=user_notes)
    # Render the search page with the form and no notes initially
    return render_template('search_notes.html', form=form, user_notes=None)

# Route to create a random note
@myapp_obj.route('/create_random_note')
@login_required
def create_random_note():
    fake = Faker()
    # Generate random English title and content
    random_title = fake.sentence(nb_words=5)[:-1]
    random_content = fake.paragraph()

    # Create a new note with the random title and content
    note = Note(
        title=random_title,
        content=random_content,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.session.add(note)
    db.session.commit()

    flash('Random Note created successfully.', 'success')
    return redirect(url_for('home'))