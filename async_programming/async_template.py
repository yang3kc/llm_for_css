"""
This script provides a template for how to use the OpenAI API in async programming and allows setting the number of concurrent requests.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI, AsyncOpenAI
import asyncio
from pydantic import BaseModel, Field

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
# Here we define a pydantic model to validate the output
# The data model should be consistent with the schema defined in the prompt
class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive.",
        ge=-1,
        le=1,
    )
    explanation: str = Field(description="Explanation of the sentiment score.")


#######################################
# Here we define a function to limit the number of concurrent requests
# The code is borrowed from https://gist.github.com/benfasoli/650a57923ab1951e1cb6355f033cbc8b
def limit_concurrency(tasks, number_of_concurrent_tasks):
    """
    Decorate coroutines to limit concurrency.
    Enforces a limit on the number of coroutines that can run concurrently in higher level asyncio-compatible concurrency managers like asyncio.gather(coroutines)
    """
    semaphore = asyncio.Semaphore(number_of_concurrent_tasks)

    async def with_concurrency_limit(task):
        async with semaphore:
            return await task

    return [with_concurrency_limit(task) for task in tasks]


#######################################
# Let's define a function to process the text message
async_client = AsyncOpenAI()


async def process_text_message_async(text_message):
    print(f"Working on text message: {text_message}")
    completion = await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        # Remember to turn the JSON mode on
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_instruction.format(text_message=text_message),
            },
        ],
    )

    senti_score_result = Sentiment.model_validate_json(
        completion.choices[0].message.content
    )
    # Async programming won't maintain the order of the results, so we need to return a dictionary with the input text message as well
    result = {
        "text_message": text_message,
        "chatgpt_response": senti_score_result.model_dump(),
    }
    return result


async def async_main():
    tasks = [process_text_message_async(text_message) for text_message in text_messages]
    async_results = await asyncio.gather(
        # Here we set the max number of concurrent requests to 3
        # For your case, you can set it to bigger values such as 20 or 100 if memory is not an issue
        # We will also return the exceptions
        *limit_concurrency(tasks, number_of_concurrent_tasks=3),
        return_exceptions=True,
    )
    return async_results


async_results = asyncio.run(async_main())

for result in async_results:
    # Here we check if the result is an exception
    # You might need to re-try the failed requests later
    if isinstance(result, Exception):
        print(f"Error: {result}")
    else:
        print(result)
