from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from twatter.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                                            DataRequired(),
                                            Length(min=4, max=20)])
    email = StringField('Email', validators=[
                                        DataRequired(),
                                        Email()])
    password = PasswordField('Password', validators=[
                                                DataRequired(),
                                                EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                                                DataRequired(),
                                                                EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already taken')

    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                                            DataRequired(),
                                            Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
                                                DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
