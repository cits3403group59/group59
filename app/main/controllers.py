import os, secrets
from PIL import Image
from flask import redirect, url_for, flash, request, current_app, render_template
from flask_login import login_required, current_user,logout_user
from werkzeug.datastructures import FileStorage
from app import db
from app.forms import SettingsForm
from app.models import User, FriendRequest, UserData
from datetime import datetime
from flask import jsonify, session
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


@main.route('/api/userdata/<int:user_id>', methods=['GET'])
@login_required
def get_user_data(user_id):
    
    cur_user_id = current_user.id
    
    if not cur_user_id:
        return jsonify({"error": "Not logged in"}), 403
    
    cur_user = User.query.get_or_404(cur_user_id)
    
    if not cur_user.is_a_friend(user_id) and cur_user_id != user_id:
        # user_id is not friend of current user and current user is not the user id 
        return jsonify({"error": "Unauthorized access"}), 403
    
    # # Use user_id from the URL or session, here we assume user_id from session for the logged-in user
    # if current_user.id != user_id:
    #     return jsonify({"error": "Unauthorized access"}), 403

    # # Parse start and end dates from the query parameters
    # start_str = request.args.get('start')
    # end_str = request.args.get('end')

    # try:
    #     start_date = datetime.strptime(start_str, '%Y-%m-%d').date() if start_str else None
    #     end_date = datetime.strptime(end_str, '%Y-%m-%d').date() if end_str else None
    # except ValueError:
    #     return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    # Fetch user data between the given dates
    user = User.query.get_or_404(user_id)  # Fetch the user from the database
    
    # Get the data between the dates
    #data = user.get_data_between(start_date, end_date)
    
    data = user.get_alltime_data()

    # Return the data in the required format
    return jsonify([
        {
            'date': d.date.strftime('%Y-%m-%d'),
            'sleep_hours': d.sleep_hours,
            'coffee_intake': d.coffee_intake,
            'social_media': d.social_media,
            'daily_steps': d.daily_steps,
            'exercise_hours': d.exercise_hours,
            'screen_time': d.screen_time,
            'work_time': d.work_time,
            'study_time': d.study_time,
            'social_time': d.social_time,
            'alcohol': d.alcohol,
            'wake_up_time': d.wake_up_time,
            'transportation': d.transportation,
            'mood': d.mood,
            'bed_time': d.bed_time,
            'money_spent': d.money_spent
        }
        for d in data
    ])
    
@main.route('/submit-survey', methods=['POST'])
@login_required
def submit_survey():
    """Handle submission of the manual data entry survey"""
    # Get the form data from the JavaScript
    form_data = request.get_json()
    
    # Parse the date from form data or use current date
    date_str = form_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Validate that the selected date is not in the future
    if selected_date > datetime.now().date():
        return jsonify({
            "success": False, 
            "message": "Cannot submit data for future dates."
        }), 400
    
    # Check if entry already exists for this user and date
    existing_entry = UserData.query.filter_by(
        user_id=current_user.id,
        date=selected_date
    ).first()
        
    if existing_entry:
        existing_entry.sleep_hours = str(form_data.get('1', '')) if form_data.get('1') else None
        existing_entry.coffee_intake = str(form_data.get('2', '')) if form_data.get('2') else None
        existing_entry.social_media = str(form_data.get('3', '')) if form_data.get('3') else None
        existing_entry.daily_steps = str(form_data.get('4', '')) if form_data.get('4') else None
        existing_entry.exercise_hours = str(form_data.get('5', '')) if form_data.get('5') else None
        existing_entry.screen_time = str(form_data.get('6', '')) if form_data.get('6') else None
        existing_entry.work_time = str(form_data.get('7', '')) if form_data.get('7') else None
        existing_entry.study_time = str(form_data.get('8', '')) if form_data.get('8') else None
        existing_entry.social_time = str(form_data.get('9', '')) if form_data.get('9') else None
        existing_entry.alcohol = str(form_data.get('10', '')) if form_data.get('10') else None
        
        # Update text input fields
        existing_entry.wake_up_time = form_data.get('11')
        existing_entry.transportation = form_data.get('12')
        existing_entry.mood = str(form_data.get('13', '')) if form_data.get('13') else None  # CHANGED: Now stores text value like "Happy"
        existing_entry.bed_time = form_data.get('14')
        money_spent_value = form_data.get('15')
        if money_spent_value:
            try:
                # CHANGED: Added rounding to ensure 2 decimal places
                existing_entry.money_spent = round(float(money_spent_value), 2)
            except ValueError:
                existing_entry.money_spent = None
        
    else:
        # Create a new survey record
        survey = UserData.from_form_data(current_user.id, form_data)
        db.session.add(survey)
    
    # Save to database
    db.session.commit()
    
    return jsonify({"success": True, "message": "Survey data saved successfully"})

@main.route('/check-survey-data')
@login_required
def check_survey_data():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Check if entry exists for this user and date
    existing_entry = UserData.query.filter_by(
        user_id=current_user.id,
        date=selected_date
    ).first()
    
    if existing_entry:
        return jsonify({
            "exists": True,
            "survey": {
                "1": existing_entry.sleep_hours,
                "2": existing_entry.coffee_intake,
                "3": existing_entry.social_media,
                "4": existing_entry.daily_steps,
                "5": existing_entry.exercise_hours,
                "6": existing_entry.screen_time,
                "7": existing_entry.work_time,
                "8": existing_entry.study_time,
                "9": existing_entry.social_time,
                "10": existing_entry.alcohol,
                "11": existing_entry.wake_up_time,
                "12": existing_entry.transportation,
                "13": existing_entry.mood,
                "14": existing_entry.bed_time,
                "15": existing_entry.money_spent
            }
        })
    else:
        return jsonify({"exists": False})
