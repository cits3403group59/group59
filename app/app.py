from flask import Flask, render_template

app = Flask(__name__)

# Route for the introductory page
@app.route('/')
def introductory():
    return render_template('introductory.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)