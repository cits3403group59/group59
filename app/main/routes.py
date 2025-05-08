"""
A python file containing the routes for the Flask main.

Contains all request handlers.
"""
from . import main  # Import the blueprint
from flask import render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import FriendRequest, User, UserData
from app.forms import FindFriendForm, RemoveFriendForm, SettingsForm
from flask_wtf import FlaskForm
from .controllers import (
    accept_request, send_request, deny_request, cancel_request,
    remove_friend, settings_controller
)
from datetime import datetime

# Route for the introductory page
@main.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the visualise data page
@main.route('/visualise-my-data')
def vis_my_data():
    return render_template('visualise_my_data.html')

# Route for the visualise twin data page
@main.route('/visualise-twin-data')
def vis_twin_data():
    return render_template('visualise_twin_data.html')

"""
TOOD: Do this using ORM User.query.all() instead of raw SQL
"""
########################## Display SQL data in html page ##########################
@main.route('/visualise-friend-data', methods=['GET'])
def vis_friend_data():
    # db_path = os.path.join(application.instance_path, 'carbon_copy.db')
    # conn = sqlite3.connect(db_path)
    # conn.row_factory = sqlite3.Row
    # cursor = conn.cursor() # create a cursor object
    # cursor.execute("SELECT * FROM user") # query the database
    # data = cursor.fetchall() # fetch all results
    # conn.close() # close the databse 
    
    # print(data)  # Add this temporarily

    # return render_template('visualise_friend_data.html', data=data) # render page by passing data 
    return render_template('visualise_friend_data.html')

# Route for upload data page
@main.route('/upload-data')
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@main.route('/manual-data')
def manual_data():
    return render_template('manual-data.html')


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
    
    from app import db
    
    if existing_entry:
        # Update existing entry
        existing_entry.sleep_hours = int(form_data.get('1'))
        existing_entry.coffee_intake = int(form_data.get('2'))
        existing_entry.social_media = int(form_data.get('3'))
        existing_entry.daily_steps = int(form_data.get('4'))
        existing_entry.exercise_minutes = int(form_data.get('5'))
        existing_entry.screen_time = int(form_data.get('6'))
        existing_entry.work_time = int(form_data.get('7'))
        existing_entry.study_time = int(form_data.get('8'))
        existing_entry.social_time = int(form_data.get('9'))
        existing_entry.alcohol = int(form_data.get('10'))
        
        # Update text input fields
        existing_entry.wake_up_time = form_data.get('11')
        existing_entry.transportation = form_data.get('12')
        existing_entry.mood = form_data.get('13')
        existing_entry.bed_time = form_data.get('14')
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
                "5": existing_entry.exercise_minutes,
                "6": existing_entry.screen_time,
                "7": existing_entry.work_time,
                "8": existing_entry.study_time,
                "9": existing_entry.social_time,
                "10": existing_entry.alcohol,
                "11": existing_entry.wake_up_time,
                "12": existing_entry.transportation,
                "13": existing_entry.mood,
                "14": existing_entry.bed_time
            }
        })
    else:
        return jsonify({"exists": False})


# Route for settings page
@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # Pass to logic handler in controllers.py
    return settings_controller()

# Route for share data page
@main.route('/share-data')
def share_data():
    return render_template('share-data.html')

# Route for manage friends page
@main.route('/manage-friends', methods=['GET'])
@login_required
def manage_friends():
    friends = current_user.get_user_friends()  # Get the user's friends
    search_query = request.args.get('search', '').lower()  # Get the search query from the URL

    # Filter friends based on the search query
    if search_query:
        friends = [friend for friend in friends if search_query in friend.first_name.lower() or search_query in friend.last_name.lower() or search_query in friend.email.lower()]

    # Create a RemoveFriendForm instance
    forms = {friend.id: RemoveFriendForm() for friend in friends}

    return render_template('manage_friends.html', friends=friends, forms=forms)

# Route for friend requests page
@main.route('/friend-requests')
@login_required
def friend_requests():
    form = FlaskForm()  
    return render_template('friend_request.html', form=form)

@main.route('/find-friends', methods=['GET', 'POST'])
@login_required
def find_friends():
    form = FindFriendForm()  # Create an instance of the form

    if form.validate_on_submit():  # Check if the form is submitted and valid
        search_email = form.email.data  # Get the email input from the form
        
        # Use the method to find the friend by email
        friend = current_user.find_friend_by_email(search_email)
        
        if friend:
            # Check ig the friend is the current user
            if friend.id == current_user.id:
                return render_template('find_friends.html', form=form, friend=friend, is_found=True, is_already_friends=False, request_exists=False, is_self=True)
                            
            # Check if the users are already friends
            if friend in current_user.friends:
                # If already friends, disable the friend request button
                return render_template('find_friends.html', form=form, friend=friend, is_found=True, is_already_friends=True, request_exists=False)
            
            # Check if a friend request already exists
            existing_request = FriendRequest.query.filter(
                ((FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == friend.id)) |
                ((FriendRequest.sender_id == friend.id) & (FriendRequest.receiver_id == current_user.id))
            ).first()
            
            if existing_request:
                flash("Friend request already exists.")
                return render_template('find_friends.html', form=form, friend=friend, is_found=True, is_already_friends=False, request_exists=True)
            
            # If not friends and no existing request, show friend request button
            return render_template('find_friends.html', form=form, friend=friend, is_found=True, is_already_friends=False, request_exists=False)
        
        else:
            flash("No user found with that email.")
            return render_template('find_friends.html', form=form, is_found=False, is_already_friends=False, request_exists=False)

    return render_template('find_friends.html', form=form, is_found=None, is_already_friends=False, request_exists=False)
