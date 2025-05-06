import os, secrets
from PIL import Image
from flask import redirect, url_for, flash, request, current_app, render_template
from flask_login import login_required, current_user,logout_user
from werkzeug.datastructures import FileStorage
from app import db
from app.forms import SettingsForm
from app.models import User, FriendRequest
from . import main  # Import the Blueprint

@main.route('/friend-request/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    current_user.accept_friend_request(request)
    flash("Friend request accepted.")
    return redirect(url_for('main.friend_requests'))

@main.route('/friend-request/send/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    receiver = User.query.get_or_404(user_id)
    try:
        current_user.send_friend_request(receiver)
        flash("Friend request sent.")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.find_friends'))

@main.route('/friend-request/<int:request_id>/deny', methods=['POST'])
@login_required
def deny_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    try:
        current_user.deny_friend_request(request)
        flash('Friend request denied.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.friend_requests'))

@main.route('/friend-request/<int:request_id>/cancel', methods=['POST'])
@login_required
def cancel_request(request_id):
    request = FriendRequest.query.get_or_404(request_id)
    try:
        current_user.cancel_friend_request(request)
        flash('Friend request canceled.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.friend_requests'))

@main.route('/friend/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    friend = User.query.get_or_404(user_id)
    try:
        current_user.remove_friend(friend)
        flash('Friend removed.')
    except ValueError as e:
        flash(str(e))
    return redirect(url_for('main.manage_friends'))

# save uploaded avatar
def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    # /app/static/profile_pics/
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn
    )
    output_size = (200, 200)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn

def settings_controller():
    form = SettingsForm()
    # GET: prefill form fields
    if request.method == 'GET':
        form.email.data      = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data  = current_user.last_name
        # Do not prefill password or file fields
        form.password.data = ''
        if hasattr(form, 'confirm_password'):
            form.confirm_password.data = ''

    # Handle POST
    if request.method == 'POST':
        # Determine if this is a delete request (password entered in delete section)
        delete_pw = request.form.get('delete_password', '').strip()
        if delete_pw:
            # User requested deletion
            if current_user.check_password(delete_pw):
                user = current_user._get_current_object()
                logout_user()
                db.session.delete(user)
                db.session.commit()
                flash('Your account has been deleted.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Incorrect password. Account not deleted.', 'danger')
                # Stop further processing, re-render
                return render_template('settings.html', form=form)
        # Else, regular settings update
        if form.validate_on_submit():
            # Update basic info
            current_user.email      = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name  = form.last_name.data

            # Update password if provided
            if form.password.data:
                current_user.set_password(form.password.data)

            # Process profile image if uploaded
            image = form.profile_image.data
            if isinstance(image, FileStorage) and image.filename:
                current_user.profile_image = save_image(image)

            db.session.commit()
            flash('Your settings have been updated.', 'success')
        else:
            flash('Please correct the errors in the form.', 'danger')

    return render_template('settings.html', form=form)
