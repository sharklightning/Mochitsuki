import os
from forms import WelcomeForm
from mochitsuki import *
from flask import Flask, render_template, url_for, request, flash
from logging import DEBUG

#load ENV variable
configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("WTF_KEY")

app.logger.setLevel(DEBUG)

selections = []

def store_selections(textinput, model):
    selections.append(dict(
        textinput = textinput,
        model = model
    ))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WelcomeForm()
    if form.validate_on_submit():
        textinput = form.textinput.data
        model = form.model.data
        store_selections(textinput, model)
        flash("Request submitted: {}".format(textinput))
        app.logger.debug("MODEL= " + model + ", INPUT= " + textinput)
    return render_template('index.html', form=form)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         textinput = request.form['text-input']
#         model = request.form['model']
#         store_selections(textinput, model)
#         flash("Request to {} successfully submitted".format(model))
#         # app.logger.debug("MODEL= " + model + "INPUT= " + textinput)
#     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')