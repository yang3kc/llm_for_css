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
    The output should be in JSON format and follow the following schema:
    --------------
    ```json
    {{
        'score': 0.1,
        'explanation': '...'
    }}
     ```
    """

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
        "url": "/v1/chat/completions",
        "body": {
            # This is what you would have in your Chat Completions API call
            "model": "gpt-3.5-turbo",
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_instruction.format(text_message=text_message),
                },
            ],
        },
    }

    tasks.append(task)


#######################################
# Write tasks to a file
task_file_name = "text_message_tasks.jsonl"
with open(task_file_name, "w") as f:
    for task in tasks:
        f.write(json.dumps(task) + "\n")
