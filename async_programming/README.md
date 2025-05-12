# TL;DR

Here is a [template](/async_programming/async_template.py) script to process text messages with async programming.
It allows you to set a max number of concurrent requests to the API and a timeout for each request.
It also uses tqdm to show the progress of the requests.
You can use the script as a starting point for your own implementation.

# Introduction

If you have a large number of text messages to process, querying the API for them one by one might take a while and most the time would be spent waiting for the responses.

Luckily, OpenAI allows sending multiple queries simultaneously to the API (async programming).
Note that different users might have different [rate limits](https://platform.openai.com/docs/guides/rate-limits/usage-tiers).
This feature means that while you are waiting for the response, you can process other text messages, greatly saving your time.

Here is my own experience.
I created a [tool](https://github.com/yang3kc/daily_arxiv_digest) to filter the new papers on arXiv everyday to save my time.
It runs the abstracts of new papers through ChatGPT and has it classify them.
The old implementation does this paper by paper in order, taking a few minutes to finish about 100 papers.
Although this is not slow at all, I decided to give async programming a try.
With the new implementation, it only takes a few seconds to process all the papers now, over x50 faster!

# Warning

Async programming is complicated, and you might run into all sorts of issues if you don't know what you are doing.
My suggestion is that you should only consider this approach when you absolutely need it.
If you don't have that many text messages to process, you can just use a for loop.
If you are not in a rush, you should also consider the new [batch API](/batch_processing), which is much easier to handle and costs only half the price.

# Async programming

Assuming you want to give async programming a try, let's first do a comparison with the traditional implementation.
The full code can be found [here](/async_programming/compare_sync_async.py).

Assuming we have a list of text messages that we want to evaluate the sentiment of:

```python
text_messages = [
    "The service here is very good!",
    "The service here is good.",
    "The service here is ok.",
    "The service here is not very good.",
    "The service here is terrible!",
]
```
The prompt would be the same as before.

## Sync implementation
Let's define a sync function to query the API:

```python
client = OpenAI()

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

```

Running it with a for loop is straight forward:

```python
sync_results = []
for text_message in text_messages:
    sync_result = process_text_message(text_message)
    sync_results.append(sync_result)
```

## Async implementation

Now let's define an async function to query the API:
```python
async_client = AsyncOpenAI()

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
```
The code is similar to the sync function above.
The main difference is that the `async_client` is an `AsyncOpenAI` object instead of an `OpenAI` object.
And we add the `async` keyword to the function name and the `await` keyword to the function call.

We can no longer use for loop to process the text messages with the async function any more. Instead, we will use `asyncio.gather`.

```python
import asyncio

async def async_main():
    async_results = await asyncio.gather(
        *[process_text_message_async(text_message) for text_message in text_messages]
    )
    return async_results

async_results = asyncio.run(async_main())
for result in async_results:
    print(result)
```

I benchmarked the performance of the two implementations and found that the async implementation is much faster: 14.08s to 2.59s.
The improvement will be more significant if you have more text messages to process.

# A template script

The implementation above has some issues.
If you have, say, 1,000 messages to process, `asyncio.gather` will try to fire up all of them simultaneously, potentially leading to memory overflows.
Doing so could also result in rate limit errors since OpenAI has rate limits for the number of requests per minute and number of tokens per minute.
To avoid hitting these limits, we can set a maximum number of concurrent requests to the API.
This can be implemented using `asyncio.Semaphore`.

This part can be complicated, so I create a [template script](/async_programming/async_template.py) to help you get started.
It also has some other nice features, like setting a timeout for each request and using tqdm to show the progress.
You might still need to add more code to handle other errors to make your application more robust, though.