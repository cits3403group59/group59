import unittest
import multiprocessing
import datetime
import threading


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.alert import Alert

from app import create_app, db
from app.models import User
from app.config import TestConfig

localHost = "http://127.0.0.1:5000/"

class SystemTests(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        
        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        
        return super().setUp()
        
    def addUser(self, first_name, last_name, email, password, dob, terms_accepted):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            terms_accepted=terms_accepted
        )
        user.set_password(password)  # Hash the password
        db.session.add(user)
        db.session.commit()
        return user
    
    def addFriend(self, user1, user2):
        user1.friends.append(user2)
        user2.friends.append(user1)
        db.session.commit()
    
    def test_sign_up(self):
        print("################ TESTING SIGN UP #######################")
        fname = "olivia"
        lname = "fitzgerald"
        email = "123@student.uwa.edu.au"
        password = "olivia"
        dob = datetime.datetime(2001, 1, 1)

        # start at homepage
        self.driver.get(localHost)

        sign_up = self.driver.find_element(By.ID, "sign-up")
        sign_up.click()

        # wait for page to render 
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "first_name"))
        )

        # this uses the flask form fields not html element ids
        self.driver.find_element(By.ID, "first_name").send_keys(fname)
        self.driver.find_element(By.ID, "last_name").send_keys(lname)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "dob").send_keys(dob.strftime("%d/%m/%Y"))
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password").send_keys(password)
        self.driver.find_element(By.ID, "terms_accepted").click()
        self.driver.find_element(By.ID, "submitBtn").click()

        WebDriverWait(self.driver, 5).until(
            expected_conditions.url_contains("/login")
        )

        print("Successfully signed up. Now at login page:", self.driver.current_url)
        self.assertEqual(localHost+"login", self.driver.current_url)
        
    def test_log_in(self):
        print("################ TESTING LOG IN #######################")
        fname = "olivia"
        lname = "fitzgerald"
        email = "123@student.uwa.edu.au"
        password = "olivia"
        dob = datetime.datetime(2001, 1, 1)
        user1 = self.addUser(fname, lname, email, password, dob, True)

        self.driver.get(localHost)

        log_in = self.driver.find_element(By.ID, "log-in")
        log_in.click()
        
        WebDriverWait(self.driver, 5).until(
            expected_conditions.url_changes(localHost)
        )

        # wait for page to render 
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "email"))
        )

        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submitBtn").click()
        
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_to_be(localHost) # This will wait until the URL is the homepage
        )

        print("Successfully logged in. Home page:", self.driver.current_url)

        # "sign-up-log-in" element is hidden 
        self.assertNotIn("sign-up-log-in", self.driver.page_source)

    
    def login(self, email, password):
        # starting from the manual data upload page 
        self.driver.get(localHost)
        
        # click login button 
        log_in = self.driver.find_element(By.ID, "log-in")
        log_in.click()
        
        print("THIS SHOULD BE THE LOGIN PAGE")
        print(self.driver.current_url)

        # we aren't logged in so we must log in 
        email_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "password")
        submit_btn = self.driver.find_element(By.ID, "submitBtn")

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_btn.click()
        
        print("THIS SHOULD BE THE HOME PAGE")
        print(self.driver.current_url)
        
    def enter_data(self):
        print("Starting to enter data")
        # Question 1: Sleep hours
        sleep_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "sleep-hours"))
        )
        sleep_input.send_keys("8")
        
        # Click Next
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 2: Coffee cups
        coffee_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "coffee-cups"))
        )
        coffee_input.send_keys("2")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 3: Social media platform (select option 1 - Instagram)
        social_option = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".question[data-question='3'] .option[data-value='1']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", social_option)
        self.driver.execute_script("arguments[0].click()", social_option)
        next_button = self.driver.find_element(By.ID, "next-btn")
        self.driver.execute_script("arguments[0].click();", next_button)

        # Question 4: Steps
        steps_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "daily-steps"))
        )
        steps_input.send_keys("8000")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 5: Exercise hours
        exercise_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "exercise-hours"))
        )
        exercise_input.send_keys("1.5")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 6: Screen time
        screen_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "screen-time"))
        )
        screen_input.send_keys("3.5")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 7: Work time
        work_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "work-time"))
        )
        work_input.send_keys("8")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 8: Study time
        study_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "study-time"))
        )
        study_input.send_keys("2")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 9: Social time
        social_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "social-time"))
        )
        social_input.send_keys("1.5")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 10: Alcohol drinks
        alcohol_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "alcohol-cups"))
        )
        alcohol_input.send_keys("1")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 11: Wake up time
        wake_up_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "wake-up-time"))
        )
        wake_up_input.send_keys("07:30AM")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 12: Transportation mode (select option 1 - Public Transport)
        transport_option = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".question[data-question='12'] .option[data-value='1']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", transport_option)
        self.driver.execute_script("arguments[0].click()", transport_option)
        self.driver.execute_script("arguments[0].click();", next_button)
        
        # Question 13: Mood (select option 1 - Happy)
        mood_option = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".question[data-question='13'] .option[data-value='1']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", mood_option)
        self.driver.execute_script("arguments[0].click();", mood_option)
        #self.driver.find_element(By.ID, "next-btn").click()
        self.driver.execute_script("arguments[0].click();", next_button)

        
        # Question 14: Bed time
        bed_time_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "bed-time"))
        )
        bed_time_input.send_keys("06:00PM")
        self.driver.find_element(By.ID, "next-btn").click()
        
        # Question 15: Money spent
        money_input = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "money-spent"))
        )
        money_input.send_keys("45.50")
        
        # Submit the form (final next-btn click should submit)
        self.driver.find_element(By.ID, "next-btn").click()
        
    def test_upload_data_page(self):
        print("##################### TESTING UPLOAD DATA ##################")
        fname = "olivia"
        lname = "fitzgerald"
        email = "123@student.uwa.edu.au"
        password = "olivia"
        dob = datetime.datetime(2001, 1, 1)
        
        user1 = self.addUser(fname, lname, email, password, dob, True)
        
        self.login(email, password)
        
        # we are now on the home page and need to navigate to the upload data page
        self.driver.get(localHost + "manual-data")
        print("THIS SHOULD BE MANUAL DATA:", self.driver.current_url)
        
        # use enter data helpter function
        self.enter_data()
        
        # Wait for the alert to appear
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present()
        )

        # Switch to the alert
        alert = Alert(self.driver)
        print("Alert was present")

        print("ALERT TEXT", alert.text)
        
        # Accept the alert
        alert.accept()
        print("Alert was present and accepted")
        
        self.driver.switch_to.default_content()
        print("switched to main window")
        print(self.driver.current_url)

        # Wait for the URL to change to home page
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_to_be(localHost)
        )

        self.assertTrue(localHost, self.driver.current_url)
        
    def test_visualise_my_data(self):
        print("##################### TESTING VISUALISE MY DATA ##################")
        fname = "olivia"
        lname = "fitzgerald"
        email = "123@student.uwa.edu.au"
        password = "olivia"
        dob = datetime.datetime(2001, 1, 1)
        
        # manually add user to db
        user1 = self.addUser(fname, lname, email, password, dob, True)
        
        # login (starts on home page)
        self.login(email, password)
        
        # we are now on the home page and need to navigate to the upload data page
        self.driver.get(localHost + "manual-data")
        print("THIS SHOULD BE MANUAL DATA:", self.driver.current_url)
        
        # use enter data helpter function
        self.enter_data()   
        
        # Wait for the alert to appear
        WebDriverWait(self.driver, 5).until(
            expected_conditions.alert_is_present()
        )

        # Switch to the alert
        alert = Alert(self.driver)
        print("Alert was present")

        print("ALERT TEXT", alert.text)
        
        # Accept the alert
        alert.accept()
        print("Alert was present and accepted")
        
        self.driver.switch_to.default_content()
        print("switched to main window")
        print(self.driver.current_url)

        # Wait for the URL to change to home page
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_to_be(localHost)
        )
        
        # Wait for link to be clickable
        visualise_toggle = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, "vis-dropdown"))
        )
        visualise_toggle.click()
        
        # navigate to the visualise my data page
        myDataBtn = self.driver.find_element(By.ID, 'vis-my-data')
        myDataBtn.click()
        
        # wait for page to change to my data 
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_to_be(localHost + "visualise-my-data")
        )
        
        # check if the data has rendered
        is_ready = WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return window.canvasDataReady === true;")
        )
        
        self.assertTrue(is_ready)
        
    def test_find_friends(self):
        print("##################### TESTING FIND FRIENDS ##################")
        fname1 = "olivia"
        lname1 = "fitzgerald"
        email1 = "123@student.uwa.edu.au"
        password1 = "olivia"
        dob1 = datetime.datetime(2001, 1, 1)
        
        fname2 = "matthew"
        lname2 = "daggit"
        email2 = "mdag@uwa.edu.au"
        password2 = "matthew"
        dob2 = datetime.datetime(2001,1,1)
        
        # add 2 users to database
        user1 = self.addUser(fname1, lname1, email1, password1, dob1, True)
        user2 = self.addUser(fname2, lname2, email2, password2, dob2, True)
        
        # login as user 1
        self.login(email1, password1)
        
        # we are now on the home page and need to navigate to the find friends
        self.driver.get(localHost + "find-friends")
        print("THIS SHOULD BE FIND FRIENDS", self.driver.current_url)
        
        # we should now try search for user2
        email_field = self.driver.find_element(By.ID, "email")
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        
        email_field.send_keys(email2)
        submit_btn.click()
        
        # wait for the friend-card element to appear
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "friend-card"))
        )
        
        # auser 2 exists in database, but they are not friends so they should have an enabled button that with id send-request
        self.assertTrue(
            self.driver.find_element(By.ID, "send-request").is_displayed(),
            "The 'send-request' button is not displayed."
        )
    
    def test_manage_friends(self):
        print("##################### TESTING MANAGE FRIENDS ##################")
        fname1 = "olivia"
        lname1 = "fitzgerald"
        email1 = "123@student.uwa.edu.au"
        password1 = "olivia"
        dob1 = datetime.datetime(2001, 1, 1)
        
        fname2 = "matthew"
        lname2 = "daggit"
        email2 = "mdag@uwa.edu.au"
        password2 = "matthew"
        dob2 = datetime.datetime(2001,1,1)
        
        # add 2 users to database
        user1 = self.addUser(fname1, lname1, email1, password1, dob1, True)
        user2 = self.addUser(fname2, lname2, email2, password2, dob2, True)
        
        # add friend relationship
        self.addFriend(user1, user2)
        
        # login as user 1
        self.login(email1, password1)
        
        # we are now on the home page and need to navigate to the find friends
        self.driver.get(localHost + "manage-friends")
        print("THIS SHOULD BE MANAGE FRIENDS", self.driver.current_url)
        
        # search for user 2 to test the search function
        email_field = self.driver.find_element(By.ID, "email")
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        
        email_field.send_keys(email2)
        submit_btn.click()     
        
        # wait for the friend-card element to appear
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "friend-card"))
        )
        
        # # remove user 2
        remove_btn = self.driver.find_element(By.ID, "removeBtn")
        remove_btn.click()
        
        # wait for confirm modal
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, 'confirm-modal'))
        )
        
        # confirm remove friend
        confirm_remove_btn = self.driver.find_element(By.ID, "confirm-remove-btn")
        confirm_remove_btn.click()        
        
        # there should be no more friend card 
        self.assertNotIn("friend-card", self.driver.page_source)
        
    def tearDown(self):
        self.server_thread.terminate()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return super().tearDown()
        

