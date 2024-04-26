"""
This script demonstrates how to use the OpenAI API to perform sentiment analysis on text messages.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI

text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."
user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.0,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
)

print(completion.choices[0].message.content)
