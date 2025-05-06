"""
A python file containing the routes for the Flask main.

Contains all request handlers.
"""
from . import main  # Import the blueprint
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import FriendRequest, User
from app.forms import FindFriendForm, RemoveFriendForm, SettingsForm
from flask_wtf import FlaskForm
from .controllers import (
    accept_request, send_request, deny_request, cancel_request,
    remove_friend, settings_controller
)

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
########################## Display SQL data in html page ##########################
@main.route('/visualise-friend-data', methods=['GET'])
@login_required
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
@login_required
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@main.route('/manual-data')
@login_required
def manual_data():
    return render_template('manual-data.html')

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
