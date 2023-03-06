import openai
import re
import os
import httpx
import logging
import asyncio
import json
from dotenv import load_dotenv
from pprint import pprint as pp
from print_response import print_response


def configure():
    load_dotenv()


async def query_gpt(text, model, prompt_selection):
    """Queries OpenAI to generate a flashcard.

    Args:
        text: plain text containing the paragraphs you would like to include in the prompt for processing
        model: the OpenAI model you would like to ingest your prompt
        promt: a custom prompt
    """

    if prompt_selection == 'default':
        use_default(text, model)
    if prompt_selection == 'code':
        use_code(text, model)

def use_code(text, model):
    openai.api_key = os.getenv("OPENAI_KEY")

    final_prompt = f"Input:\nif temp <= 0:\n\tprint(\"It’s freezing\")\nelif temp >= 100:\n\tprint(\"It’s boiling\")\nelse:\n\tprint(\"It's alright\")\nOutput:\nQ: Write a conditional statement in python that prints different strings depending on whether the temperature is less than 0, greater than 100, or something else.\n---\n```python\nif temp <= 0:\n\tprint(\"It’s freezing\")\nelif temp >= 100:\n\tprint(\"It’s boiling\")\nelse:\n\tprint(\"It\'s alright\")\n```\n\nInput:\npopulous_countries = [\"China\", \"India\", \"USA\", \"Indonesia\", \"Brazil\"]\npopulous_countries[2] = \"United States\"\npopulous_countries.append(\"Pakistan\")\n\nOutput:\nQ: Write python code that changes the third element of the list populous_countries to \"United States\", and adds \"Pakistan\" to the end of the list.\n`populous_countries = [\"China\", \"India\", \"USA\", \"Indonesia\", \"Brazil\"]`\n---\n```python\npopulous_countries[2] = \"United States\"\npopulous_countries.append(\"Pakistan\")\n```\nInput:\n{text}\nOutput:"

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

    with open(f"src/cards/temp.md", "w+") as temp:
        temp.write(f"{answer}")

def use_default(text, model):
    openai.api_key = os.getenv("OPENAI_KEY")

    paragraphs = re.split('\n\n+', text)

    for i, paragraph in enumerate(paragraphs):
        final_prompt = f"Please perform the following steps on the text given after \"Text input:\" below \n- Extract and condense the most important details of the text\n- Use these bullet points to generate flash card style question and answer pairs\n- Always begin a question with \"Q:\"\n- Always begin an answer with \"A:\"\n- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block\n-Be sure to include any important context in the question portion\n- Format the answers in concise bullet points\n- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above\nText input: \n" + f"{paragraph}"

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
    parentid = None
    if parent != None:
        for obj in deck_list['docs']:
            if parent in obj['name'] == parent:
                parentid = obj['id']
        if parentid != None:
            payload = {"name": name, "parent-id": parentid}
        else: # if it does not exist, create it
            parent_req_payload = {"name": parent}
            parent_resp = httpx.post(site, auth=apikey, headers=headers, json=parent_req_payload)
            parent_resp_json = json.loads(parent_resp.text)
            parentid = parent_resp_json['id']
            payload = {"name": name, "parent-id": parentid}
    else:
        payload = {"name": name}

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

    # content = data
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
