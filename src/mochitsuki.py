import openai
import re
import os
import httpx 
import logging
import asyncio
import json
from prompts import Prompt
from dotenv import load_dotenv
from pprint import pprint as pp
from print_response import print_response

def configure():
    load_dotenv()

async def query_gpt(text, model="text-davinci-003", prompt=Prompt()):
    """Queries OpenAI to generate a flashcard.

    Args:
        text: plain text containing the paragraphs you would like to include in the prompt for processing
        model: the OpenAI model you would like to ingest your prompt
        promt: a custom prompt
    """
    openai.api_key = os.getenv("OPENAI_KEY")

    
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

        with open(f"src/temp/temp_{i}.md", "w+") as temp:
            temp.write(f"{answer}")
        
        with open(f"src/temp/temp_{i}.md", "r") as f:
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

        with open(f"src/cards/flashcard_{i}.md", "w") as file:
            contents = "".join(contents)
            file.write(contents)

        os.remove(f"src/temp/temp_{i}.md")

def set_deck(name, parent=None):
    """Checks if a deck exists in Mochi and creates a new deck if it doesn't.
    
    Args:
        name: The name of the deck you would like to add to or create
        parent: If you are creating a nested deck, supply the name of the parent here
    """

    # set variables and logging config
    mochikey = os.getenv("MOCHI_KEY")
    apikey = (mochikey, '')
    site = 'https://app.mochi.cards/api/decks'
    headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
                }
    
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger()

    # check if deck already exists
    getdeck_resp = httpx.get(site, auth=apikey)
    deck_list = json.loads(getdeck_resp.text)
    for obj in deck_list['docs']:
        if name in obj['name'] == name:
            return obj['id']

    # check if a parent-id was supplied
    if parent != None:
        for obj in deck_list['docs']:
            if parent in obj['name'] == parent:
                parentid = obj['id']
        payload = { "name": name, "parent-id": parentid }
    else:
        payload = { "name": name }

    # make a new deck if it doesn't exist
    makedeck_resp = httpx.post(site, auth=apikey, headers=headers, json=payload)
    deck = json.loads(makedeck_resp.text)
    return deck['id']

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

def new_card(file, deck=None):
    """Creates new cards based on the response from GPT
    
    Args: 
        file: a file containing the response from GPT, usually 'src/cards/flashcard_{i}.md'
        deck: the deck-id of the deck you would like to add cards to
    """

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
                    "deck-id": deck,
                  }

        card = httpx.post(site, auth=apikey, headers=headers, json=payload)


