import os
from dotenv import load_dotenv
from forms import TsukiForm
from tsuki import Tsuki
from flask import Flask, render_template, url_for, request, flash, redirect, session
from logging import DEBUG

def configure():
    load_dotenv()

configure()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("WTF_KEY")

app.logger.setLevel(DEBUG)

@app.route('/', methods=['GET', 'POST'])
async def index():
    form = TsukiForm()
    # if session.get('model'):
    #     form.model.data = session.get('model') # Check if model is stored in the session and persist it if so
    if form.validate_on_submit():
        textinput = form.textinput.data
        model = form.model.data
        deck = form.deck.data
        prompt_selection = form.prompt.data
        parent = form.parent.data
        
        if (parent != None) and (parent != ''):
            tsuki = Tsuki(textinput, model, deck, prompt_selection, parent)
            # deck_id = tsuki.set_deck()
        else:
            tsuki = Tsuki(textinput, model, deck, prompt_selection)
            # deck_id = tsuki.set_deck()

        tsuki.query_gpt()
        
        for file in os.listdir("src/cards/"):
            if file != '.gitignore':
                file_name = "src/cards/" + file
                tsuki.set_card(file_name)
                os.remove(file_name)

        # persist choices for duration of session
        session['model'] = model
        session['deck'] = deck
        session['prompt_selection'] = prompt_selection
        session['parent'] = parent

        # debugging and logging
        app.logger.debug("MODEL= " + model + ", INPUT= " + textinput)
        flash("Request submitted to: {}".format(model))

        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

