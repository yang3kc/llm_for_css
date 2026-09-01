"""
This script sends a basic query to a model running locally with Ollama.

Before running it, start Ollama and download the model:

    ollama pull gemma4:e2b

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI

#######################################
# Prompt-related

text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."

#######################################
# Query the local model

# Ollama serves an OpenAI-compatible API on your machine.
# Point the client at it; the API key is required by the SDK but ignored by Ollama.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

completion = client.chat.completions.create(
    model="gemma4:e2b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
    # gemma4 "thinks" before answering by default. Turn it off for short tasks like this one.
    reasoning_effort="none",
)

print(completion.choices[0].message.content)
