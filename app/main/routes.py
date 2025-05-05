"""
A python file containing the routes for the Flask main.

Contains all request handlers.
"""
from . import main  # Import the blueprint
from flask import render_template

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

# Route for settings page
@main.route('/settings')
def settings():
    return render_template('settings.html')

# Route for share data page
@main.route('/share-data')
def share_data():
    return render_template('share-data.html')

