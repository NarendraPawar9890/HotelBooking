from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):

    name = StringField("Name", validators=[
        DataRequired(), Length(min=2, max=100)
    ])

    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])

    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=4, max=100)
    ])

    submit = SubmitField("Register")

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])

    password = PasswordField("Password", validators=[
        DataRequired()
    ])

    submit = SubmitField("Login")
