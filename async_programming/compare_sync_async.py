"""
This script compares the sync and async version of the same code.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI, AsyncOpenAI
import asyncio
from pydantic import BaseModel, Field
import time

#######################################
# Prompt-related

# Here assume we have multiple messages to process
text_messages = [
    "The service here is very good!",
    "The service here is good.",
    "The service here is ok.",
    "The service here is not very good.",
    "The service here is terrible!",
]

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = """
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    """


#######################################
# Here we define a pydantic model to validate the output
class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive."
    )
    explanation: str = Field(description="Explanation of the sentiment score.")


#######################################
# Let's first try the traditional method to query the API
client = OpenAI()

# The logic here is very simple, we use a for loop to process each text message one by one and store the results in a list
# We will also time it


# Let's first define a function to process the text message
def process_text_message(text_message):
    print(f"Working on text message: {text_message}")
    response = client.responses.parse(
        model="gpt-4.1-mini",
        temperature=0.0,
        text_format=Sentiment,
        instructions=system_prompt,
        input=user_instruction.format(text_message=text_message),
    )

    senti_score_result = response.output_parsed
    result = {
        "text_message": text_message,
        "chatgpt_response": senti_score_result.model_dump(),
    }
    return result


print("Traditional method:")
start_time = time.perf_counter()
sync_results = []
for text_message in text_messages:
    sync_result = process_text_message(text_message)
    sync_results.append(sync_result)

end_time = time.perf_counter()
print(f"Traditional method done in {end_time - start_time:.2f} seconds.")
for result in sync_results:
    print(result)

#######################################
# Now let's use async programming
# We will need to use the async client
async_client = AsyncOpenAI()


# Similarly, we can define a function to process the text message
# Note that the difference with the sync version is the `async` and `await` keywords
async def process_text_message_async(text_message):
    print(f"Working on text message: {text_message}")
    response = await async_client.responses.parse(
        model="gpt-4.1-mini",
        temperature=0.0,
        text_format=Sentiment,
        instructions=system_prompt,
        input=user_instruction.format(text_message=text_message),
    )

    senti_score_result = response.output_parsed
    result = {
        "text_message": text_message,
        "chatgpt_response": senti_score_result.model_dump(),
    }
    return result


# We can no longer use for loop to process the text messages
# Instead, we will use asyncio.gather
async def async_main():
    async_results = await asyncio.gather(
        *[process_text_message_async(text_message) for text_message in text_messages]
    )
    return async_results


print("Async method:")
start_time = time.perf_counter()
async_results = asyncio.run(async_main())
end_time = time.perf_counter()
print(f"Async method done in {end_time - start_time:.2f} seconds.")
for result in async_results:
    print(result)
