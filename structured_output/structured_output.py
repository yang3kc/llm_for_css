"""
This script demonstrates how to use the JSON mode of OpenAI's API to obtain structured output and parse (validate) the output.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI
from pydantic import BaseModel, Field

#######################################
# Prompt-related
text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

# Note that to use JSON mode, you have to explicitly specify the schema of the output in the prompt
user_instruction = f"""
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
# Query the API
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.0,
    # Remember to turn the JSON mode on
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
)


#######################################
# Here we define a pydantic model to validate the output
# The data model should be consistent with the schema defined in the prompt
class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive.",
        ge=-1,
        le=1,
    )
    explanation: str = Field(description="Explanation of the sentiment score.")


senti_score_result = Sentiment.model_validate_json(
    completion.choices[0].message.content
)

# Print the result as a dictionary
senti_score_dict = senti_score_result.model_dump()
print(senti_score_dict)

# You can get the score and explanation directly
print(senti_score_dict["score"])
print(senti_score_dict["explanation"])

# You can also obtain the JSON string
# senti_score_json = senti_score_result.model_dump_json()
# print(senti_score_json)
