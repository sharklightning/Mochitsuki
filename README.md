# Mochitsuki
> **Mochitsuki**: The Japanese tradition of "mochi pounding" at the end of rice harvest, when the grain is pounded into soft dough to enjoy throughout the holiday after a long harvest season.

## Introduction

Mochitsuki takes any text input. By default it generates flashcards using OpenAI's Turbo GPT-3.5 model, in markdown format. 

Currently, Mochitsuki automatically imports cards to [Mochi](https://mochi.cards/) (this requires Mochi Pro subscription). 

I plan to add an option in the near future to dump the cards as an Anki or Mochi export so that you manually import them to your preferred flashcard application without Mochi pro. 

## Prerequisites
You will need Docker installed in order to run Mochitsuki on your local machine. 

You will need your own OpenAI account and API key. You can sign up for one [here](https://openai.com/product).

A Mochi pro subscription so you can use their API.  

## Usage
Clone this git repository to your local machine  
```git clone https://github.com/sharklightning/Mochitsuki.git```

Change into the Mochitsuki directory  
```cd Mochitsuki```

Create a .env file to store your API keys:  
```touch src/.env```

Add your OpenAI api key into the .env file:  
```echo OPENAI_KEY=your-api-key-here > src/.env```

Optionally, add your Mochi api key as well:  
```echo MOCHI_KEY=your-api-key-here >> src/.env```

You will also need to generate a long random number in whatever way you like and store it as the WTF_KEY for the web form to work correctly:  
```echo WTF_KEY=<long-random-number-here> >> src/.env```

Build the Mochitsuki docker image  
```docker build -t tsuki-image .```

Run a container instance of the Mochitsuki image  
```docker run -dp 127.0.0.1:5000:5000 tsuki-image```

Alternatively, if you would like to run Mochitsuki in development mode so that your local changes to the source code will be synced to the running container instance, use:  
```docker-compose up --build```

Navigate to 127.0.0.1:5000 in the URL field of your web browser. 

## Roadmap
- build in concurrency and rate limiting safegaurds for large batches
- add support for anki export/import
- develop browser extension for converting highlighted text
- add ocr 
- mobile app
