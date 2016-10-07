from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    name = TextField('Full Name', [DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone', validators=[Length(10)])