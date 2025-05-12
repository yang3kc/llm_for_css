"""
This script demonstrates how to use the structured output of OpenAI's API.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI
from pydantic import BaseModel, Field


#######################################
# Prompt-related
text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"""
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    """


#######################################
# Here we define a pydantic model to validate the output
# The data model should be consistent with the schema defined in the prompt
# Ideally, we also want to define the lower and upper bounds of the score, but OpenAI's API doesn't support it currently
# See https://platform.openai.com/docs/guides/structured-outputs#some-type-specific-keywords-are-not-yet-supported for details
class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive."
    )
    explanation: str = Field(description="Explanation of the sentiment score.")


#######################################
# Query the API
client = OpenAI()

response = client.responses.parse(
    model="gpt-4.1-mini",
    temperature=0.0,
    instructions=system_prompt,
    input=user_instruction,
    text_format=Sentiment,
)

parsed_output = response.output_parsed
# Print the result as a dictionary
senti_score_dict = parsed_output.model_dump()
print(senti_score_dict)

# You can get the score and explanation directly
print(f"Score: {parsed_output.score}")
print(f"Explanation: {parsed_output.explanation}")
