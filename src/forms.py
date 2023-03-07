from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length

class TsukiForm(FlaskForm):
    model = RadioField('Pick a model', choices=[('text-davinci-003', 'Davinci'), ('text-curie-001', 'Curie'), ('text-babbage-001', 'Babbage')])
    deck = StringField(validators=[InputRequired()])
    parent = StringField()
    prompt = SelectField(u'Prompt: ', choices=[('default', 'Text card'), ('code', 'Code')])
    textinput = TextAreaField(validators=[InputRequired(), Length(1, 2250)])
