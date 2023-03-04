import openai
import re
import os
import httpx 
import logging
from prompts import Prompt
from dotenv import load_dotenv
from pprint import pprint as pp
from print_response import print_response

def configure():
    load_dotenv()

def query_gpt(input_file, model="text-davinci-003", prompt=Prompt()):
    """Queries OpenAI to generate a flashcard.

    Args:
        input_file: a plain text file containing the paragraphs you would like to include in the prompt for processing
        model: the OpenAI model you would like to ingest your prompt

    """
    openai.api_key = os.getenv("OPENAI_KEY")

    with open(input_file, "r") as temp:
        text = temp.read()
    
    paragraphs = re.split('\n\n+', text)

    for i, paragraph in enumerate(paragraphs):
        final_prompt = prompt.prompt + f"{paragraph}"
        
        response = openai.Completion.create(
            engine=model,
            prompt=final_prompt,
            temperature=0.7,
            max_tokens=3400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        answer = response.choices[0].text.strip()

        with open(f"temp/temp_{i}.md", "w+") as temp:
            temp.write(f"{answer}")
        
        with open(f"temp/temp_{i}.md", "r") as f:
            contents = f.readlines()
 
        inc = 0
        while inc <= len(contents):
            try:
                if contents[inc][0] == 'A':
                    contents.insert(inc, "---\n")
                    inc += 1
                inc += 1
            except:
                break

        with open(f"cards/flashcard_{i}.md", "w") as file:
            contents = "".join(contents)
            file.write(contents)

        os.remove(f"temp/temp_{i}.md")

def new_deck(name):
    """Creates a new deck in Mochi
    
    Args:
        name: The name of the deck you would like to create
        parent: If you are creating a nested deck, supply the parent here
    """

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger()

    # Optional debugging statement
    # breakpoint()  # py3.7+
    # import pdb; pdb.set_trace()  # py3.6-

    mochikey = os.getenv("MOCHI_KEY")
    apikey = (mochikey, '')
    site = 'https://app.mochi.cards/api/decks'
    headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
                }
    payload = {
                "name": name,
                "parent-id": "LrTAyWQ1"
                }
    
    deck = httpx.post(site, auth=apikey, headers=headers, json=payload)

    return deck

def format_data(data):
    content = []
    string = ''
    for i in data:
        if i == '\n':
            content.append(string)
            string = ''
        else:
            string += i
    content.append(string)  # Add the final string to the content list
    return content

def new_card(file):

    with open(file, "rt", encoding="utf-8") as f:
        data = f.readlines()
    
    content = format_data(data)

    for card in content:
        # Create a basic logger using a common configuration
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logger = logging.getLogger()

        mochikey = os.getenv("MOCHI_KEY")
        apikey = (mochikey, '')
        site = 'https://app.mochi.cards/api/cards/'

        headers = {
                    "Content-Type": "application/json"
                  }
        payload = {
                    "content": card,
                    "deck-id": "LrTAyWQ1",
                  }

        card = httpx.post(site, auth=apikey, headers=headers, json=payload)

        return card


