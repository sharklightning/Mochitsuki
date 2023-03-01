# Mochitsuki
> **Mochitsuki**: The Japanese tradition of "mochi pounding" at the end of rice harvest, when the grain is pounded into soft dough to enjoy throughout the holiday after a long harvest season.

## Introduction

Mochitsuki takes any text input. By default it generates flashcards using OpenAI's GPT-3 Davinci model, in markdown format. 

Optionally you can configure Mochitsuki to automatically import to [Mochi](https://mochi.cards/) (this requires Mochi Pro subscription). Alternatively, you can dump the cards as an Anki or Mochi export and manually import them to your preferred flashcard application. 

## Prerequisites

You will need your own OpenAI account and API key. You can sign up for one [here](https://openai.com/product).

Optionally, you can use Mochitsuki to automate the step of importing your cards to Mochi. This allows you to go from text input to imported flash cards in a single step, but requires a Mochi pro subscription so you can use their API.   

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

## Usage


## Roadmap
- add anki support
- add ocr 
