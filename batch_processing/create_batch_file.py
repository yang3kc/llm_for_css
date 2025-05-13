"""
This script creates a batch file that can be used to submit to the batch API.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

import json

#######################################
# We will use the same text messages as example
text_messages = [
    "The service here is very good!",
    "The service here is good.",
    "The service here is ok.",
    "The service here is not very good.",
    "The service here is terrible!",
]

#######################################
# Prompt-related
system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = """
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    """

#######################################
# JSON schema for the response
# For the batch API, you have to specify the schema manually
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
# Create tasks
tasks = []
for index, text_message in enumerate(text_messages):
    task = {
        # The API won't return the input text message, so we need a unique ID for each task
        # This way we can merge the results back with the input text message
        # Instead of generating the ID on the fly, it's recommended to assign a unique ID to each input message at the beginning
        "custom_id": f"text_message_{index}",
        "method": "POST",
        "url": "/v1/responses",
        "body": {
            # This is what you would have in your Chat Completions API call
            "model": "gpt-4o-mini",
            "temperature": 0.0,
            "instructions": system_prompt,
            "input": user_instruction.format(text_message=text_message),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "sentiment",
                    "strict": True,
                    "schema": sentiment_json_schema,
                }
            },
        },
    }

    tasks.append(task)


#######################################
# Write tasks to a file
task_file_name = "text_message_tasks.jsonl"
with open(task_file_name, "w") as f:
    for task in tasks:
        f.write(json.dumps(task) + "\n")
