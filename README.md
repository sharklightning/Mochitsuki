# Mochitsuki
> **Mochitsuki**: The Japanese tradition of "mochi pounding" at the end of rice harvest, when the grain is pounded into soft dough to enjoy throughout the holiday after a long harvest season.

## Introduction

Mochitsuki takes any text input. By default it generates flashcards using OpenAI's GPT-3 Davinci model, in markdown format. 

Optionally you can configure Mochitsuki to automatically import to [Mochi](https://mochi.cards/) (this requires Mochi Pro subscription). Alternatively, you can dump the cards as an Anki or Mochi export and manually import them to your preferred flashcard application. 

## Prerequisites
You will need docker installed in order to run Mochitsuki on your local machine. 

You will need your own OpenAI account and API key. You can sign up for one [here](https://openai.com/product).

Optionally, you can use Mochitsuki to automate the step of importing your cards to Mochi. This allows you to go from text input to imported flash cards in a single step, but requires a Mochi pro subscription so you can use their API.   

## Usage
Clone this git repository to your local machine  
```git clone https://github.com/sharklightning/Mochitsuki.git```

Change into the Mochitsuki directory  
```cd Mochitsuki```

Create a .env file to store your API keys:  
```touch app/src/.env```

Add your OpenAI api key into the .env file:  
```echo OPENAI_KEY=your-api-key-here > app/src/.env```

Optionally, add your Mochi api key as well:  
```echo MOCHI_KEY=your-api-key-here >> app/src/.env```

Build the Mochitsuki docker image  
```docker build -t tsuki-image .```

Run a container instance of the Mochitsuki image  
```docker run -dp 127.0.0.1:5000:5000 tsuki-image```

Navigate to 127.0.0.1:5000 in the URL field of your web browser. 

## Prompt

Currently, the working default prompt is:
```
Please perform the following steps on the text given after "Text input:" below 
- Extract and condense the most important details of the text
- Use these bullet points to generate flash card style question and answer pairs
- Always begin a question with "Q:"
- Always begin an answer with "A:"
- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block
- Format the answers in concise bullet points
- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above
Text input: 
```
Users are encouraged to improve upon this prompt or modify it to suit your particular needs. 

It is one of our goals on this project to build a library of purpose suited prompts. Please do not hesitate to submit a PR if you think you're prompt might be useful to others. 

## Roadmap
- add anki support
- add ocr 
- develop browser extension for converting highlighted text
- mobile app
