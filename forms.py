from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    email = StringField('E-Mail')
    phone = StringField('Phone')
