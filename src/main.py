import os
from dotenv import load_dotenv
from forms import TsukiForm
from tsuki import Tsuki
from flask import Flask, render_template, url_for, request, flash, redirect, session
from logging import DEBUG

THIS IS JUST A TEST

def configure():
    load_dotenv()

configure()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("WTF_KEY")

app.logger.setLevel(DEBUG)

@app.route('/', methods=['GET', 'POST'])
async def index():
    form = TsukiForm()
    if form.validate_on_submit():
        textinput = form.textinput.data
        deck = form.deck.data
        prompt_selection = form.prompt.data
        parent = form.parent.data
        
        if parent:
            tsuki = Tsuki(textinput, deck, prompt_selection, parent)
        else:
            tsuki = Tsuki(textinput, deck, prompt_selection)

        tokens, cards = tsuki.query_gpt()
        
        for file in os.listdir("src/cards/"):
            if file != '.gitignore':
                file_name = "src/cards/" + file
                tsuki.set_card(file_name)
                os.remove(file_name)

        app.logger.debug("INPUT= " + textinput)
        flash("Request successful. {} cards created. Tokens used: {}".format(cards, tokens))

        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

