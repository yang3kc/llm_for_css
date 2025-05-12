"""
This script demonstrates how to use the OpenAI API to perform sentiment analysis on text messages.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI

text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."
user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    temperature=0,
    instructions=system_prompt,
    input=user_instruction,
)

print(response.output_text)
