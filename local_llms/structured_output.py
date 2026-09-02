"""
This script obtains structured output from a model running locally with Ollama.

Before running it, start Ollama and download the model:

    ollama pull gemma4:e2b

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

# --8<-- [start:code]
from openai import OpenAI
from pydantic import BaseModel, Field

#######################################
# Prompt-related

text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."


#######################################
# Here we define a pydantic model to validate the output
class Sentiment(BaseModel):
    score: float = Field(
        ge=-1,
        le=1,
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive.",
    )
    explanation: str = Field(description="Explanation of the sentiment score.")


#######################################
# Query the local model

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

completion = client.chat.completions.parse(
    model="gemma4:e2b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
    response_format=Sentiment,
    reasoning_effort="none",
)

parsed_output = completion.choices[0].message.parsed

# Print the result as a dictionary
print(parsed_output.model_dump())

# You can get the score and explanation directly
print(f"Score: {parsed_output.score}")
print(f"Explanation: {parsed_output.explanation}")
# --8<-- [end:code]
