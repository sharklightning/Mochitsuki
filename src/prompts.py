class Prompt:
    """Used to instatiate a new prompt object"""
    
    default_prompt = f"Please perform the following steps on the text given after \"Text input:\" below \n- Extract and condense the most important details of the text\n- Use these bullet points to generate flash card style question and answer pairs\n- Always begin a question with \"Q:\"\n- Always begin an answer with \"A:\"\n- If the text contains code blocks, use code examples in your  questions and answers as appropriate, using markdown to format the examples as a code block\n-Be sure to include any important context in the question portion\n- Format the answers in concise bullet points\n- Respond to this prompt with only the final form of the questions and answers, formatted according to the instructions above\nText input: \n"
    
    def __init__(self, prompt=default_prompt):
        self.prompt = prompt
