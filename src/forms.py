from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length

class TsukiForm(FlaskForm):
    prompt = RadioField(choices=[('default', 'Text prompt'), ('code', 'Code prompt')])
    deck = StringField(validators=[InputRequired()])
    parent = StringField()
    textinput = TextAreaField(validators=[InputRequired(), Length(1, 2250)])
