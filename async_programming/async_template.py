"""
This script provides a template for how to use the OpenAI API in async programming and allows setting the number of concurrent requests.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import AsyncOpenAI
import asyncio
from pydantic import BaseModel, Field
from tqdm.asyncio import tqdm_asyncio

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
# Let's define a function to process the text message
async_client = AsyncOpenAI()


async def process_text_message_async(text_message):
    response = await async_client.responses.parse(
        model="gpt-4.1-mini",
        temperature=0.0,
        instructions=system_prompt,
        input=user_instruction.format(text_message=text_message),
        text_format=Sentiment,
    )

    senti_score_result = response.output_parsed
    # Async programming won't maintain the order of the results, so we need to return a dictionary with the input text message as well
    result = {
        "text_message": text_message,
        "response": senti_score_result.model_dump(),
    }
    return result


async def async_main(text_messages, concurrent_tasks=3):
    # Create tasks properly
    tasks = []
    for text_message in text_messages:
        task = asyncio.create_task(process_text_message_async(text_message))
        tasks.append(task)

    # Apply concurrency limit
    semaphore = asyncio.Semaphore(concurrent_tasks)

    async def bounded_task(task):
        async with semaphore:
            return await task

    # Create bounded tasks
    bounded_tasks = [bounded_task(task) for task in tasks]

    # Gather results with tqdm
    async_results = await tqdm_asyncio.gather(*bounded_tasks)
    return async_results


if __name__ == "__main__":
    async_results = asyncio.run(async_main(text_messages, concurrent_tasks=3))
    for result in async_results:
        # Here we check if the result is an exception
        # You might need to re-try the failed requests later
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(result)
