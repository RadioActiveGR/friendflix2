from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, DataRequired

class PostForm(FlaskForm):
    title = StringField(validators=[Required()])
    body = TextAreaField(validators=[Required()])
    submit = SubmitField()
