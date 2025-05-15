"""
This script demonstrates how to use threading to process text messages.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from openai import OpenAI
from pydantic import BaseModel, Field
import time
from tqdm.contrib.concurrent import thread_map

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


# Initialize the client
client = OpenAI()


# Define a function to process the text message
def process_text_message(text_message):
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


N_THREADS = 3
print(f"Threading method with {N_THREADS} threads:")
start_time = time.perf_counter()

# Here we use the thread_map function from the tqdm.contrib.concurrent module
# It is a wrapper around the threading.Thread class, and it will automatically handle the threading for you
# It will also show a progress bar
threading_results = thread_map(
    process_text_message,
    text_messages,
    max_workers=N_THREADS,
    desc="Processing text messages",
)

end_time = time.perf_counter()
print(f"Threading method done in {end_time - start_time:.2f} seconds.")

for result in threading_results:
    print(result)
