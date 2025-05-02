"""
Controller for the application MVC architecture. 
"""

import sqlite3
from flask import render_template
from app import application

# Display SQL data in html page
@application.route('/data', methods=['GET'])
def view_data():
    conn = sqlite3.connect('carbon_copy.db') # connect to the database
    cursor = conn.cursor() # create a cursor object
    cursor.execute("SELECT * FROM User LIMIT 10") # query the database
    data = cursor.fetchall() # fetch all results
    conn.close() # close the databse 
    return render_template('visualise-my-data.html', data=data) # render page by passing data 