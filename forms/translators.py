from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class NewsForm(FlaskForm):
    text = TextAreaField("text")
    language = TextAreaField("language")
