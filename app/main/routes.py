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
from app import db


# Route for the introductory page
@main.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the visualise data page
@main.route('/visualise-my-data')
@login_required
def vis_my_data():
    return render_template('visualise_my_data.html')

# Route for the visualise twin data page
@main.route('/visualise-twin-data')
@login_required
def vis_twin_data():
    return render_template('visualise_twin_data.html')

"""
TOOD: Do this using ORM User.query.all() instead of raw SQL
"""
@main.route('/visualise-friend-data')
@login_required
def vis_friend_data():
    return render_template('visualise_friend_data.html')

# Route for upload data page
@main.route('/upload-data')
@login_required
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@main.route('/manual-data')
@login_required
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
    
    # Process numeric fields - convert to appropriate type when possible
    # Define which fields should be numeric
    numeric_fields = {
        '1': 'float',    # sleep_hours (decimal hours)
        '2': 'int',      # coffee_cups (integer)
        '4': 'int',      # daily_steps (integer)
        '5': 'float',    # exercise_hours (decimal hours)
        '6': 'float',    # screen_time (decimal hours)
        '7': 'float',    # work_time (decimal hours)
        '8': 'float',    # study_time (decimal hours)
        '9': 'float',    # social_time (decimal hours)
        '10': 'int'      # alcohol (integer cups)
    }
    
    # Convert fields to proper types
    for field, field_type in numeric_fields.items():
        if field in form_data and form_data[field]:
            try:
                if field_type == 'int':
                    form_data[field] = int(float(form_data[field]))
                elif field_type == 'float':
                    form_data[field] = round(float(form_data[field]), 1)  # 1 decimal place
            except (ValueError, TypeError):
                # If conversion fails, set to None
                form_data[field] = None
        else:
            form_data[field] = None
    
    # Check if entry already exists for this user and date
    existing_entry = UserData.query.filter_by(
        user_id=current_user.id,
        date=selected_date
    ).first()
        
    if existing_entry:
        # Update existing entry with the new values
        existing_entry.sleep_hours = form_data.get('1')
        existing_entry.coffee_intake = form_data.get('2')
        existing_entry.social_media = form_data.get('3')
        existing_entry.daily_steps = form_data.get('4')
        existing_entry.exercise_hours = form_data.get('5')  # Now using exercise_hours
        existing_entry.screen_time = form_data.get('6')
        existing_entry.work_time = form_data.get('7')
        existing_entry.study_time = form_data.get('8')
        existing_entry.social_time = form_data.get('9')
        existing_entry.alcohol = form_data.get('10')
        
        # Update text input fields
        existing_entry.wake_up_time = form_data.get('11')
        existing_entry.transportation = form_data.get('12')
        existing_entry.mood = form_data.get('13')
        existing_entry.bed_time = form_data.get('14')
        
        # Handle money spent
        money_spent_value = form_data.get('15')
        if money_spent_value:
            try:
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
        # All values must be converted to strings for the frontend
        return jsonify({
            "exists": True,
            "survey": {
                "1": str(existing_entry.sleep_hours) if existing_entry.sleep_hours is not None else None,
                "2": str(existing_entry.coffee_intake) if existing_entry.coffee_intake is not None else None,
                "3": existing_entry.social_media,
                "4": str(existing_entry.daily_steps) if existing_entry.daily_steps is not None else None,
                "5": str(existing_entry.exercise_hours) if existing_entry.exercise_hours is not None else None,  # Changed from exercise_minutes
                "6": str(existing_entry.screen_time) if existing_entry.screen_time is not None else None,
                "7": str(existing_entry.work_time) if existing_entry.work_time is not None else None,
                "8": str(existing_entry.study_time) if existing_entry.study_time is not None else None,
                "9": str(existing_entry.social_time) if existing_entry.social_time is not None else None,
                "10": str(existing_entry.alcohol) if existing_entry.alcohol is not None else None,
                "11": existing_entry.wake_up_time,
                "12": existing_entry.transportation,
                "13": existing_entry.mood,
                "14": existing_entry.bed_time,
                "15": str(existing_entry.money_spent) if existing_entry.money_spent is not None else None
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
@login_required
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
