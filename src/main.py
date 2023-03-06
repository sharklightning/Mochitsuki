import os
from forms import WelcomeForm
from mochitsuki import *
from flask import Flask, render_template, url_for, request, flash, redirect, session
from logging import DEBUG

#load ENV variable
configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("WTF_KEY")

app.logger.setLevel(DEBUG)

@app.route('/', methods=['GET', 'POST'])
async def index():
    form = WelcomeForm()
    # if session.get('model'):
    #     form.model.data = session.get('model') # Check if model is stored in the session and persist it if so
    if form.validate_on_submit():
        textinput = form.textinput.data
        model = form.model.data
        deck = form.deck.data
        parent = form.parent.data
        prompt_selection = form.prompt.data

        if (parent != None) and (parent != ''):
            deck_id = set_deck(deck, parent)
        else:
            deck_id = set_deck(deck)

        session['model'] = model
        app.logger.debug("MODEL= " + model + ", INPUT= " + textinput)
        flash("Request submitted to: {}".format(model))

        await query_gpt(textinput, model, prompt_selection)
        for file in os.listdir("src/cards/"):
            if file != '.gitignore':
                file_name = "src/cards/" + file
                new_card(file_name, deck_id)
                os.remove(file_name)

        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

