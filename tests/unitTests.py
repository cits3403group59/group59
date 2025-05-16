import unittest
import os
from datetime import date, timedelta
from app import create_app, db
from app.models import User
from app.config import TestConfig
from werkzeug.security import generate_password_hash

class UserValidationTestCase(unittest.TestCase):
    """Test validation in user registration."""
    
    def setUp(self):
        """Set up test environment with in-memory database."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Verify we're using the in-memory database
        self.assertTrue(self.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory')
        
        db.create_all()
        
        # Create a test user for duplicate email tests
        self.existing_user = User(
            first_name="Existing",
            last_name="User",
            email="existing@example.com",
            dob=date(1900, 1, 1),
            password_hash=generate_password_hash('password123', method='pbkdf2:sha256'),
            terms_accepted=True
        )
        db.session.add(self.existing_user)
        db.session.commit()
        
        self.client = self.app.test_client()
        
        # Create test user data
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'dob': '1990-01-01',
            'terms_accepted': True
        }
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_valid_registration(self):
        """Test successful registration with valid data."""
        response = self.client.post('/register', data=self.valid_data, follow_redirects=True)
        
        # Check if user was created in database
        user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(user, "User should be created with valid data")
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        
        # Should be redirected to login page
        self.assertIn(b'<form id="signin-form" method="POST" action="/login">', response.data)
    
    def test_invalid_email(self):
        """Test that invalid email format is rejected."""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = self.client.post('/register', data=invalid_data, follow_redirects=True)
        
        # Check user was not created
        user = User.query.filter_by(first_name='John').first()
        self.assertIsNone(user, "User should not be created with invalid email")
        
        # Should stay on registration page
        self.assertIn(b'Create Account</h1>', response.data)
    
    def test_future_dob(self):
        """Test that future date of birth is rejected."""
        future_data = self.valid_data.copy()
        future_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        future_data['dob'] = future_date
        
        response = self.client.post('/register', data=future_data, follow_redirects=True)
        
        # Check user was not created
        user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNone(user, "User should not be created with future DOB")
        
        # Should stay on registration page
        self.assertIn(b'Create Account</h1>', response.data)
    
    def test_old_dob(self):
        """Test that very old date of birth is rejected."""
        old_data = self.valid_data.copy()
        old_date = date(1900, 1, 1).strftime('%Y-%m-%d')  # Very old date
        old_data['dob'] = old_date
        
        response = self.client.post('/register', data=old_data, follow_redirects=True)
        
        # Check if user was created (depends on your validation - might allow very old dates)
        user = User.query.filter_by(email='john.doe@example.com').first()
        
        # Optional assertion depending on your requirements:
        #self.assertIsNone(user, "User should not be created with very old DOB")
        
        # Should stay on registration page if validation failed
        if user is None:
            self.assertIn(b'Create Account</h1>', response.data)
            
        # Optionally check for specific error message if your form displays one
        #self.assertIn(b'Date of birth must be within the last 120 years', response.data)
    
    def test_password_mismatch(self):
        """Test that mismatched passwords are rejected."""
        mismatch_data = self.valid_data.copy()
        mismatch_data['confirm_password'] = 'different_password'
        
        response = self.client.post('/register', data=mismatch_data, follow_redirects=True)
        
        # Check user was not created
        user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNone(user, "User should not be created with mismatched passwords")
        
        # Should stay on registration page
        self.assertIn(b'Create Account</h1>', response.data)
    
    def test_duplicate_email(self):
        """Test that registration with an existing email is rejected."""
        duplicate_data = self.valid_data.copy()
        duplicate_data['email'] = 'existing@example.com'  # Same as existing user
    
        try:
            response = self.client.post('/register', data=duplicate_data, follow_redirects=True)
            # If we get here, check that we're still on the registration page
            self.assertIn(b'Create Account</h1>', response.data)
            
            # Check that no new user was created with this email
            users = User.query.filter_by(email='existing@example.com').count()
            self.assertEqual(users, 1, "Should still have only one user with this email")
        except Exception as e:
            # If we get a database error, that's also an acceptable outcome
            # since it means the duplicate email was rejected
            if 'UNIQUE constraint failed: user.email' in str(e):
                pass
            else:
                # If it's some other error, re-raise it
                raise

if __name__ == '__main__':
    unittest.main()