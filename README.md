# Mochitsuki
An open source GPT-3 flashcard generator for Mochi, Anki

> **Mochitsuki**: The Japanese tradition of "mochi pounding" at the end of rice harvest, when the grain is pounded into soft dough to enjoy throughout the holiday after a long harvest season.

## Introduction

Mochitsuki takes any text input. By default it generates flashcards using OpenAI's GPT-3 Davinci model, in markdown format. 

Optionally you can configure Mochitsuki to automatically import to Mochi (this requires Mochi Pro subscription). Alternatively, you can dump the cards as an Anki or Mochi export and manually import them to your preferred flashcard application. 

## Prerequisites

You will need your own OpenAI account and API key. You can sign up for one [here][].

Optionally, if you would like to automatically import cards/decks in Mochi, you will also need an API key from Mochi.

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

## Roadmap
- add anki support
- add ocr 
