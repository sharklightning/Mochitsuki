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
    """The Tsuki Class creates an object for interacting with the OpenAI and Mochi APIs
    
    Args:
        text:
        deck:
        prompt_selection:
        parent (optional):
    """

    def __init__(self, text, deck, prompt_selection, parent=None):
        self.text = text
        self.deck = deck
        self.prompt = prompt_selection
        self.parent = parent
        openai.api_key = os.getenv("OPENAI_KEY")

        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logger = logging.getLogger()

    def query_gpt(self):
        if self.prompt == 'default':
            token_usage, cards = self._defaultprompt()
        if self.prompt == 'code':
            token_usage, cards = self._codeprompt()
        return (token_usage, cards)

    def set_deck(self):
        """Checks if a deck exists, creates one if it doesn't, and returns the deck id"""

        # set variables
        mochikey = os.getenv("MOCHI_KEY")
        apikey = (mochikey, '')
        site = 'https://app.mochi.cards/api/decks'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        getdeck_resp = httpx.get(site, auth=apikey)
        deck_list = json.loads(getdeck_resp.text)

        # check if deck already exists
        deck = {deck['name']: deck['id'] for deck in deck_list['docs'] if deck['name'] == self.deck}
        if deck:
            return deck[self.deck]

        # if parent was passed, check if it exists and create if not
        if self.parent:
            deck = {deck['name']: deck['id'] for deck in deck_list['docs'] if deck['name'] == self.parent}
            if deck:
                parentid = deck[self.parent]
                payload = {"name": self.deck, "parent-id": parentid}
            else:
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

    def _requestchat(self, user_content, role_content):
        request = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                        {"role": "system", "content": role_content},
                        {"role": "user", "content": user_content}
                    ],
            temperature=0.7
        )
        return request

    def _defaultprompt(self):
        paragraphs = re.split('\n\n+', self.text)

        token_usage = 0
        cards = 0

        for i, paragraph in enumerate(paragraphs):

            role_content = "You are an assistant that helps to make and correctly format text for use as flashcards."
            user_content = f"Please perform the following steps on the text given after \"Text input:\" below \n- Extract and condense the most important details of the text\n- Use these bullet points to generate flash card style question and answer pairs\n- Always begin a question with \"Q:\"\n- Always begin an answer with \"A:\"\n- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block\n-Be sure to include any important context in the question portion\n- Format the answers in concise bullet points\n- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above\nText input: \n" + f"{paragraph}"

            request = self._requestchat(user_content, role_content)

            response = request['choices'][0]['message']['content']
            token_usage += int(request['usage']['total_tokens'])
            cards += 1

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

        return (token_usage, cards)

    def _codeprompt(self):
        role_content = "You are an assistant that helps to make and correctly format text for use as flashcards."
        user_content = f'Take a code snippet from the user and make a flashcard to help them learn how to code. The general format of the cards will look like this:\nQ: <insert question here>\n---\n<insert solution here>\nYou can include some code examples in the question as long as the example does not reveal the solution. Here are an examples:\nInput:\nif temp <= 0:\n    print("It’s freezing")\nelif temp >= 100:\n    print("It’s boiling")\nelse:\n    print("It\'s alright")\n\nOutput:\nQ: Write a conditional statement in python that prints different strings depending on whether the temperature is less than 0, greater than 100, or something else.\n---\n```python\nif temp <= 0:\n    print("It’s freezing")\nelif temp >= 100:\n    print("It’s boiling")\nelse:\n    print("It\'s alright")\n```\n\nInput:\npopulous_countries = ["China", "India", "USA", "Indonesia", "Brazil"]\npopulous_countries[2] = "United States"\npopulous_countries.append("Pakistan")\n\nOutput:\nQ: Write python code that changes the third element of the list populous_countries to "United States", and adds "Pakistan" to the end of the list.\n`populous_countries = ["China", "India", "USA", "Indonesia", "Brazil"]`\n---\n```python\npopulous_countries[2] = "United States"\npopulous_countries.append("Pakistan")\n```\n\nInput:\nclass Bike:\n    def __init__(self, description, condition, sale_price, cost=0):\n        self.cost = cost\n        self.sale_price = sale_price\n        self.condition = condition\n        self.description = description\nOutput:\nQ: Write the code for a class in Python called Bike that has four instance variables: cost, sale_price, condition and description.\n---\n```python\nclass Bike:\n    def __init__(self, description, condition, sale_price, cost=0):\n        self.cost = cost\n        self.sale_price = sale_price\n        self.condition = condition\n        self.description = description\n```\n\nInput:\nfrom random import randint\n\ndef run_game():\n    scores = [0, 0]\n    for i, score in enumerate(scores):\n        player_num = i +1\n        roll = randint(1, 6)\n        score += roll\n        print(f"Player {{player_num}}: {{score}} (rolled a {{roll}})")\nOutput:\nQ: Write a function in Python that uses a for loop to simulate two players rolling a dice, and prints out their scores after each roll.\n---\n```python\nfrom random import randint\n\ndef run_game():\n    scores = [0, 0]\n    for i, score in enumerate(scores):\n        player_num = i +1\n        roll = randint(1, 6)\n        score += roll\n        print(f"Player {{player_num}}: {{score}} (rolled a {{roll}})")\n```\n\nNow please complete the next example:\n\Input:\n{self.text}\nOutput:\n'

        request = self._requestchat(user_content, role_content)

        response_content = request['choices'][0]['message']['content']
        token_usage = int(request['usage']['total_tokens'])
        cards = 1

        with open(f"src/cards/temp.md", "w+") as temp:
            temp.write(f"{response_content}")

        return (token_usage, cards)
