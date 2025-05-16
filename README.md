# CITS3403 Group Project - Data Doppelganger
## Purpose of Application 
CarbonCopy is an all in one habit tracking and social platform. With the ability to connect with friends, you can compare your habits with theirs, keeping each other accountable and encouraging some friendly competition. Excitingly, there is a "find my data doppelganger" function which finds which of your friends has the most similar habits to you. 

CarbonCopy was designed with user experience in mind, the user interfaces are simple and intuitive, with no context required to navigate through the application. A simple colour scheme is maintained throughout, with various screen sizes kept in mind when rendering the web app. 

## Group Members
| Student ID    | Student Name      | GitHub Username |
| ------------- | ----------------- | --------------- |
| 23332873      | Blythe Cheung     | blythecheung    |
| 23902466      | Sharan Prabhu     | sharanp245      |
| 24279373      | Chunyu Zheng      | chunyuzheng152  |
| 23764974      | Olivia Fitzgerald | OliviaFitzgerald|

## Instructions
Note: without the secret keys in the `.env` file, this application will not run

### How to launch application:
To run the application on a local server, follow the instructions below:

Note: this requires Python 3.8 or later
```
# Activate virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# apply data base migrations
flask db upgrade

# start app
python3 carboncopy.py
```

### How to run tests:
The system tests run on a local live server, when running the system tests, please ensure your local host (http://127.0.0.1:5000/) is not running in the background prior to starting.
```
# to run all tests
python3 -m unittest tests/*Tests.py

# to run unit tests only
python3 -m unittest tests/unitTests.py

# to run system tests only
python3 -m unittest tests/systemTests.py
```


