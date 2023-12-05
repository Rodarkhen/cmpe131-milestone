# routes.py
from flask import render_template, redirect, flash, url_for, request, send_file
from flask_login import login_user, current_user, logout_user, login_required
from app import myapp_obj, db
from .models import User, Note, SharedNote
from .forms import SignUpForm, LoginForm, EditProfileForm, NoteForm, SearchForm
from datetime import datetime
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import re

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
    # Render the login template with the login form
    return render_template('login.html', form=form)

# Route for the home page
@myapp_obj.route('/home')
@login_required
def home():
    # Retrieve all notes for the current user
    user_notes = current_user.notes.all()
    # Retrieve all shared notes for the current user
    shared_notes = SharedNote.query.filter_by(shared_with_user_id=current_user.id).all()
    # Render the home template with the user's name and notes
    return render_template('home.html', name=current_user.name, user_notes=user_notes, shared_notes=shared_notes)

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
        return redirect(url_for('edit_profile'))

    # Pre-fill the form with the current user information
    form.name.data = current_user.name
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.created_at.data = current_user.created_at.strftime("%m-%d-%Y")  # Convert datetime to string for display

    # Render the edit profile template with the form
    return render_template('edit_profile.html', form=form)

# Route to Create a note
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

    # Get all shared notes associated with the current note
    shared_notes = SharedNote.query.filter_by(note_id=note.id).all()

    # Delete the shared notes
    for shared_note in shared_notes:
        db.session.delete(shared_note)

    # Delete the note itself
    db.session.delete(note)
    db.session.commit()

    flash('Note deleted successfully', 'success')
    return redirect(url_for('home'))

# Route for searching notes
@myapp_obj.route('/search_notes', methods=['GET', 'POST'])
@login_required
def search_notes():
    form = SearchForm()

    # Initialize the count of found notes
    found_notes_count = 0

    # Handle the search logic upon form submission/validation
    if form.validate_on_submit():
        search_query = form.search_query.data
        # Perform the search based on your criteria
        user_notes = current_user.notes.filter(
            (Note.title.contains(search_query)) | (Note.content.contains(search_query))).all()

        # Retrieve shared notes for the current user based on the search query
        shared_notes = SharedNote.query.join(Note).filter(
            (Note.title.contains(search_query)) | (Note.content.contains(search_query)),
            SharedNote.shared_with_user_id == current_user.id
        ).all()

        # Count the total number of found notes
        found_notes_count = len(user_notes) + len(shared_notes)

        # Render the search results page with the form and notes
        return render_template('search_notes.html', form=form, user_notes=user_notes, shared_notes=shared_notes, found_notes_count=found_notes_count)
    # Render the search page with the form and no notes initially
    return render_template('search_notes.html', form=form, user_notes=None, shared_notes=None, found_notes_count=found_notes_count)

# Route for searching notes with regular expression for both title and content
@myapp_obj.route('/search_notes_regex', methods=['GET', 'POST'])
@login_required
def search_notes_regex():
    form = SearchForm()

    # Initialize the count of found notes
    found_notes_count = 0

    # Handle the search logic upon form submission/validation
    if form.validate_on_submit():
        search_query = form.search_query.data

        # Perform the search based on regular expression criteria for both title and content
        user_notes = current_user.notes.filter(
            (Note.title.op('REGEXP')(search_query)) | (Note.content.op('REGEXP')(search_query))
        ).all()

        # Retrieve shared notes for the current user based on the search query
        shared_notes = SharedNote.query.join(Note).filter(
            (Note.title.op('REGEXP')(search_query)) | (Note.content.op('REGEXP')(search_query)),
            SharedNote.shared_with_user_id == current_user.id
        ).all()

        # Count the total number of found notes
        found_notes_count = len(user_notes) + len(shared_notes)

        # Render the search results page with the form and notes
        return render_template('search_notes_regex.html', form=form, user_notes=user_notes, shared_notes=shared_notes, found_notes_count=found_notes_count)

    # Render the search page with the form and no notes initially
    return render_template('search_notes_regex.html', form=form, user_notes=None, shared_notes=None, found_notes_count=found_notes_count)

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

# Route to generate a pdf from a note
@myapp_obj.route('/note_to_pdf/<int:note_id>', methods=['GET'])
@login_required
def note_to_pdf(note_id):
    note = Note.query.get_or_404(note_id)

    # Check if the current user is the owner of the note or a shared user
    if note.user_id == current_user.id or SharedNote.query.filter_by(note_id=note.id, shared_with_user_id=current_user.id).first():
        try:
            # Create a BytesIO object to store the PDF
            pdf_bytes = BytesIO()

            # Use ReportLab to generate the PDF with a standard letter page size (8.5 x 11 inches)
            pdf_canvas = SimpleDocTemplate(pdf_bytes, pagesize=letter)
            styles = getSampleStyleSheet()

            # Create a list to hold the content elements
            content = []

            # Add the title to the content as a Paragraph with a bold style
            title_style = styles['Title']
            content.append(Paragraph(note.title, title_style))

            # Add a space between title and content
            content.append(Spacer(1, 12))

            # Add the content to the content list as a Paragraph with a normal style
            content_style = ParagraphStyle('custom_style', parent=styles['Normal'], spaceAfter=12)
            content.append(Paragraph(note.content, content_style))

            # Build the PDF document using the content list
            pdf_canvas.build(content)

            # Reset the buffer position to the beginning
            pdf_bytes.seek(0)

            # Create a Flask response with the PDF
            response = send_file(
                pdf_bytes,
                as_attachment=True,
                download_name=f'{note.title}.pdf',  # Use note title as the filename
                mimetype='application/pdf'
            )

            return response

        except ValueError as e:
            # Flash an error message and redirect to the home page
            flash(f"Cannot generate a PDF for this note", 'error')
            return redirect(request.referrer or url_for('home'))

    else:
        flash('You do not have permission to convert this note to PDF.', 'error')
        return redirect(request.referrer or url_for('home'))

# Route to share a note to other users 
@myapp_obj.route('/notes/<int:note_id>/share', methods=['POST'])
@login_required
def share_note(note_id):
    # Get the username from the form data
    username_to_share_with = request.form.get('username')

    # Check if the username is the same as the current user's username
    if username_to_share_with == current_user.username:
        flash('You cannot share a note with yourself.', 'error')
        return redirect(url_for('home'))

    # Query the user to share with from the database
    user_to_share_with = User.query.filter_by(username=username_to_share_with).first()

    # Check if the user to share with exists
    if user_to_share_with:
        # Query the note from the database
        note = Note.query.get(note_id)

        # Check if the note exists and if the current user is the owner of the note
        if note and note.user_id == current_user.id:
            # Check if the note is already shared with the specified user
            existing_shared_note = SharedNote.query.filter_by(note_id=note.id, shared_with_user_id=user_to_share_with.id).first()

            if existing_shared_note:
                flash('Note is already shared with this user.', 'error')
            else:
                # Create a new SharedNote instance and add it to the database
                shared_note = SharedNote(note_id=note.id, shared_with_user_id=user_to_share_with.id)
                db.session.add(shared_note)
                db.session.commit()
                flash('Note shared successfully!', 'success')

        else:
            flash('You do not have permission to share this note.', 'error')
    else:
        flash('User not found.', 'error')

    # Redirect to the current note instead of the home page
    return redirect(url_for('edit_note', note_id=note_id))

# Route to view all shared notes by other users
@myapp_obj.route('/shared_notes')
@login_required
def shared_notes():
    shared_notes = SharedNote.query.filter_by(shared_with_user_id=current_user.id).all()
    return render_template('shared_notes.html', shared_notes=shared_notes)

# Route to view the specific shared notes
@myapp_obj.route('/shared_notes/<int:shared_note_id>')
@login_required
def view_shared_note(shared_note_id):
    shared_note = SharedNote.query.get(shared_note_id)

    # Check if the shared note exists and if the current user has access
    if shared_note and shared_note.shared_with_user_id == current_user.id:
        return render_template('view_shared_note.html', shared_note=shared_note)
    else:
        flash('Note not found or you do not have permission to view it.', 'error')
        return redirect(url_for('home'))

# Route to unshare or unlink a shared notes
@myapp_obj.route('/unshare_note/<int:shared_note_id>', methods=['GET', 'POST'])
@login_required
def unshare_note(shared_note_id):
    shared_note = SharedNote.query.get_or_404(shared_note_id)

    # Check if the current user is either the owner or the recipient of the shared note
    if shared_note.note.user_id == current_user.id or shared_note.shared_with_user_id == current_user.id:
        # Get the referrer URL before the form submission
        referrer = request.referrer

        # Check if the form is submitted
        if request.method == 'POST':
            # Remove the shared note from the database
            db.session.delete(shared_note)
            db.session.commit()

            flash('Note unshared successfully!', 'success')
            # Redirect back to the referrer URL or the home page if referrer is None
            return redirect(referrer or url_for('home'))

        # Render the confirmation template for unsharing
        return render_template('unshare_note.html', shared_note=shared_note)

    flash('You do not have permission to unshare this note.', 'error')
    # Redirect back to the referrer URL or the home page if referrer is None
    return redirect(referrer or url_for('home'))