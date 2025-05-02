"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
import sqlite3
from flask import render_template, redirect, url_for, session
from app import application
from flask import send_from_directory
from flask_login import login_required, current_user
from app.models import db, User, FriendRequest 
import os 

# Route for the introductory page
@application.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the visualise data page
@application.route('/visualise-my-data')
def vis_my_data():
    return render_template('visualise-my-data.html') 

# Route for the visualise twin data page
@application.route('/visualise-twin-data')
def vis_twin_data():
    return render_template('visualise-twin-data.html')

# Route for upload data page
@application.route('/upload-data')
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@application.route('/manual-data')
def manual_data():
    return render_template('manual-data.html')

# Route for settings page
@application.route('/settings')
def settings():
    return render_template('settings.html')

# Route for share data page
@application.route('/share-data')
def share_data():
    return render_template('share-data.html')

@application.route('/login')
def login_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('introductory'))
    return render_template('login_page.html')

@application.route('/signup')
def signup_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('introductory'))
    return render_template('signup_page.html')

@application.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    return redirect(url_for('introductory'))

########################## Display SQL data in html page ##########################
@application.route('/visualise-friend-data', methods=['GET'])
def vis_friend_data():
    db_path = os.path.join(application.instance_path, 'carbon_copy.db')
    conn = sqlite3.connect(db_path)  # ✅ Correct usage    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() # create a cursor object
    cursor.execute("SELECT * FROM user LIMIT 10") # query the database
    data = cursor.fetchall() # fetch all results
    conn.close() # close the databse 
    
    print(data)  # Add this temporarily

    return render_template('visualise-friend-data.html', data=data) # render page by passing data 

########################### Share Data With Friends ############################
# Share link route
# This route generates a shareable link for the user to send to their friends
@application.route('/share_link')
@login_required
def share_link():
    link = url_for('send_request', user_id=current_user.id, _external=True)
    return render_template('share_link.html', link=link)

# Route to send a friend request
# This route allows a user to send a friend request to another user
@application.route('/send_request/<int:user_id>', methods=['GET'])
@login_required
def send_request(user_id):
    if user_id == current_user.id:
        return "You can't send a friend request to yourself!"

    # Check if request already exists
    existing = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=user_id).first()
    if existing:
        return "Friend request already sent or pending!"

    new_request = FriendRequest(sender_id=current_user.id, receiver_id=user_id)
    db.session.add(new_request)
    db.session.commit()
    return "Friend request sent!"

# Route to accept a friend request
# This route allows a user to accept or deny a friend request
@application.route('/respond_request/<int:request_id>/<action>')
@login_required
def respond_request(request_id, action):
    req = FriendRequest.query.get_or_404(request_id)

    if req.receiver_id != current_user.id:
        return "Not authorized"

    if action == 'accept':
        req.status = 'accepted'
        # Add each other as friends if your app supports it
        # create mutual Friendship entries if needed
    elif action == 'deny':
        req.status = 'denied'

    db.session.commit()
    return redirect(url_for('friend_requests'))

################# THIS ISNT BEING USED ATM #######################
# Basic routes for serving HTML pages
@application.route('/')
def home():
    # Check if user is logged in
    if 'user_id' in session:
        # User is logged in, serve logged-in version
        return send_from_directory('.', 'static-introductory-loggedin.html')
    else:
        # User is not logged in, serve not-logged-in version
        return send_from_directory('.', 'static-introductory-notloggedin.html')
    
@application.route('/dashboard')
def dashboard():
    # Only allow access if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory('.', 'static-introductory-loggedin.html')

#######################################################################