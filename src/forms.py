from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

class WelcomeForm(FlaskForm):
    textinput = TextAreaField(validators=[InputRequired(), Length(1, 2250)])
    submit = SubmitField('Generate Cards')
    model = RadioField('Pick a model', choices=[('text-davinci-003', 'Davinci'), ('text-curie-001', 'Curie'), ('text-babbage-001', 'Babbage')])