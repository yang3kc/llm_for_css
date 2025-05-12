"""
This script demonstrates how to use the structured output of OpenAI's API by providing a json schema directly.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI
import json


#######################################
# Prompt-related
text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"""
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    """


#######################################
# Here we define the json schema manually.
# But note that the API has some requirements. I would suggest trying it out in the Playground first.
sentiment_json_schema = {
    "type": "object",
    "title": "Sentiment",
    "required": ["score", "explanation"],
    "properties": {
        "score": {
            "type": "number",
            "title": "Score",
            "description": "Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive.",
        },
        "explanation": {
            "type": "string",
            "title": "Explanation",
            "description": "Explanation of the sentiment score.",
        },
    },
    "additionalProperties": False,
}


#######################################
# Query the API
client = OpenAI()

# Use the json schema
response = client.responses.parse(
    model="gpt-4.1-mini",
    temperature=0.0,
    instructions=system_prompt,
    input=user_instruction,
    text={
        "format": {
            "type": "json_schema",
            "name": "sentiment",
            "strict": True,
            "schema": sentiment_json_schema,
        }
    },
)

# Note that the output won't be parsed automatically.
text_output = response.output_text

# You can print the output as a string
print(text_output)

# Or parse it yourself
# And you can check the result is valid
parsed_output = json.loads(text_output)

print(f"Score: {parsed_output['score']}")
print(f"Explanation: {parsed_output['explanation']}")
