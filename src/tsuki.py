import openai
import re
import os
import httpx
import logging
import asyncio
import json
from dotenv import load_dotenv
from print_response import print_response

class Tsuki:
    def __init__(self, text, model, deck, prompt_selection, parent=None):
        self.text = text
        self.model = model
        self.deck = deck
        self.prompt = prompt_selection
        self.parent = parent
        openai.api_key = os.getenv("OPENAI_KEY")

    def query_gpt(self):
        if self.prompt == 'default':
            self._defaultprompt()
        if self.prompt == 'code':
            self._codeprompt()
    
    def set_deck(self):
        """Checks if a deck exists, creates one if it doesn't, and returns the deck id"""

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
        # refactor the code below as:
        # deck = {deck['name']: deck['id'] for deck in deck_list['docs'] if deck['name'] == name}
        # if deck != {}:
        #     return deck[name]
        for obj in deck_list['docs']:
            if self.deck in obj['name'] == self.deck:
                return obj['id']

        # check if a parent-id was supplied
        parentid = None
        if self.parent != None:
            for obj in deck_list['docs']:
                if self.parent in obj['name'] == self.parent:
                    parentid = obj['id']
            if parentid != None:
                payload = {"name": self.deck, "parent-id": parentid}
            else: # if it does not exist, create it
                parent_req_payload = {"name": self.parent}
                parent_resp = httpx.post(site, auth=apikey, headers=headers, json=parent_req_payload)
                parent_resp_json = json.loads(parent_resp.text)
                parentid = parent_resp_json['id']
                payload = {"name": self.deck, "parent-id": parentid}
        else:
            payload = {"name": self.deck}

        # make a new deck if it doesn't exist
        makedeck_resp = httpx.post(site, auth=apikey, headers=headers, json=payload)
        _deck = json.loads(makedeck_resp.text)
        return _deck['id']

    def set_card(self, file_name):

        deck_id = self.set_deck()
        mochikey = os.getenv("MOCHI_KEY")
        apikey = (mochikey, '')
        site = 'https://app.mochi.cards/api/cards/'
        headers = {
            "Content-Type": "application/json"
        }

        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logger = logging.getLogger()
        
        with open(file_name, "rt", encoding="utf-8") as f:
            data = f.readlines()

        if self.prompt == 'default':
            content = self._format(data)
            for card in content:

                payload = {
                    "content": card,
                    "deck-id": deck_id,
                }

                httpx.post(site, auth=apikey, headers=headers, json=payload)
        else:
            content = ''.join(data)
            payload = {
                "content": content,
                "deck-id": deck_id,
            }

            httpx.post(site, auth=apikey, headers=headers, json=payload)
        

    def _format(self, data):
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

    def _request(self, prompt):
        request = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                temperature=0.7,
                max_tokens=3400,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        return request

    def _defaultprompt(self):
        paragraphs = re.split('\n\n+', self.text)

        for i, paragraph in enumerate(paragraphs):
            final_prompt = f"Please perform the following steps on the text given after \"Text input:\" below \n- Extract and condense the most important details of the text\n- Use these bullet points to generate flash card style question and answer pairs\n- Always begin a question with \"Q:\"\n- Always begin an answer with \"A:\"\n- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block\n-Be sure to include any important context in the question portion\n- Format the answers in concise bullet points\n- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above\nText input: \n" + f"{paragraph}"
            
            request = self._request(final_prompt)

            response = request.choices[0].text.strip()

            with open(f"src/temp/temp_{i}.md", "w+") as temp:
                temp.write(f"{response}")

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

    def _codeprompt(self):
        final_prompt = f"In the following examples, be sure to provide sufficient context in your questions. For example, if a function is referenced that is needed for the answer, define that function in the question.\nInput:\nif temp <= 0:\n\tprint(\"It’s freezing\")\nelif temp >= 100:\n\tprint(\"It’s boiling\")\nelse:\n\tprint(\"It's alright\")\nOutput:\nQ: Write a conditional statement in python that prints different strings depending on whether the temperature is less than 0, greater than 100, or something else.\n---\n```python\nif temp <= 0:\n\tprint(\"It’s freezing\")\nelif temp >= 100:\n\tprint(\"It’s boiling\")\nelse:\n\tprint(\"It\'s alright\")\n```\n\nInput:\npopulous_countries = [\"China\", \"India\", \"USA\", \"Indonesia\", \"Brazil\"]\npopulous_countries[2] = \"United States\"\npopulous_countries.append(\"Pakistan\")\n\nOutput:\nQ: Write python code that changes the third element of the list populous_countries to \"United States\", and adds \"Pakistan\" to the end of the list.\n`populous_countries = [\"China\", \"India\", \"USA\", \"Indonesia\", \"Brazil\"]`\n---\n```python\npopulous_countries[2] = \"United States\"\npopulous_countries.append(\"Pakistan\")\n```\nInput:\n{self.text}\nOutput:"

        request = self._request(final_prompt)

        response = request.choices[0].text.strip()

        with open(f"src/cards/temp.md", "w+") as temp:
            temp.write(f"{response}")
