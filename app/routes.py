"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
from app import app

# Route for the introductory page
@app.route('/')
def introductory():
    return render_template('introductory.html') # render temllae ad fill introductory view elements

# Run the application
if __name__ == '__main__':
    app.run(debug=True)