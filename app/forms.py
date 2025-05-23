from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Optional
from datetime import date
from wtforms.fields import DateField
from flask_wtf.file import FileField, FileAllowed


class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')  # <--- Add this
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    terms_accepted = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_dob(form, field):
        today = date.today()
        if field.data > today:
            raise ValidationError('Date of birth cannot be in the future.')
        if field.data < date(today.year - 120, today.month, today.day):
            raise ValidationError('Date of birth must be within the last 120 years.')

class FindFriendForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Search')
    
class RemoveFriendForm(FlaskForm):
    submit = SubmitField('Remove Friend')

class SettingsForm(FlaskForm):
    # Personal Info
    first_name = StringField(
        'First Name',
        validators=[DataRequired(message='Please enter your first name')]
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(message='Please enter your last name')]
    )
    profile_image = FileField(
        'Profile Picture',
        validators=[
            Optional(), FileAllowed(['jpg', 'png'], message='Only JPG and PNG files are allowed')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Please enter your email address'),
            Email(message='Please enter a valid email address')
        ]
    )
    password = PasswordField('New Password', validators=[Optional()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[Optional(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Update Settings')