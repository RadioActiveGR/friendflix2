import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, DataRequired, Email, Length, EqualTo, ValidationError

def character_check(form, field):
    excluded_chars= "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed"
            )

class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=8, max=15,
                                                                message='Password must be between 8 and 15 characters in length'), character_check])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password',
                                                                         message='Both password fields must be equal')])
    pinkey = StringField(validators=[Required(), character_check, Length(max=32, min=32, message="Length of pin must be 32.")])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit and 1 upper case letter")


class LoginForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pinkey = StringField(validators=[Required()])
    recaptcha = RecaptchaField()
    submit = SubmitField()


