import openai
import re
import os
import httpx 
import logging
from dotenv import load_dotenv
from pprint import pprint as pp
from print_response import print_response

def configure():
    load_dotenv()

def query_gpt(input_file):
    # Authenticate with the OpenAI API by setting your API key
    openai.api_key = os.getenv("OPENAI_KEY)

    # Open the text file and read its contents
    with open(input_file, "r") as temp:
        text = temp.read()
    
    # Split the text into paragraphs
    paragraphs = re.split('\n\n+', text)

    # Loop over each paragraph and generate a flashcard
    for i, paragraph in enumerate(paragraphs):
        # Set the prompt for GPT to generate a flashcard
        prompt = f"Please perform the following steps on the text given after \"Text input:\" below \n- Extract and condense the most important details of the text\n- Use these bullet points to generate flash card style question and answer pairs\n- Always begin a question with \"Q:\"\n- Always begin an answer with \"A:\"\n- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block\n-Be sure to include any important context in the question portion\n- Format the answers in concise bullet points\n- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above\nText input: \n{paragraph}"
        
        # Generate the flashcard using GPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=3400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the answer from the response
        answer = response.choices[0].text.strip()

        # Save the flashcard as a markdown file with formatting for flashcards
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

    # Create a basic logger using a common configuration
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

def new_card(file):

    with open(file, "rt", encoding="utf-8") as f:
        data = f.readlines()
    
    content = []
    string = ''
    for i in data:
        if i == '\n':
            content.append(string)
            string = ''
        else:
            string += i


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


