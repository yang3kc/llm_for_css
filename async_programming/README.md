# Introduction

If you have a large number of text messages to process, querying the API for them one by one might take a while and most the time would be spent waiting for the responses.

Luckily, the API providers, including OpenAI, allow sending multiple queries simultaneously to the API.
Note that different users might have different [rate limits](https://platform.openai.com/docs/guides/rate-limits/usage-tiers).
This feature means that while you are waiting for the response, you can process other text messages, greatly saving your time.

Here is my own experience.
I created a [tool](https://github.com/yang3kc/daily_arxiv_digest) to filter the new papers on arXiv everyday to save my time.
It runs the abstracts of new papers through ChatGPT and has it classify them.
The old implementation does this paper by paper in order, taking a few minutes to finish about 100 papers.
Although this is not slow at all, I decided to give async programming a try.
With the new implementation, it only takes a few seconds to process all the papers now, over x50 faster!

There are two ways to do this in Python: threading and async programming.
And I'll provide a template for both of them.

## TL;DR

- [Threading template](/async_programming/threading_template.py)
- [Async template](/async_programming/async_template.py)

Both templates allow you to set a max number of concurrent requests to the API and a timeout for each request.
They also use tqdm to show the progress of the requests.
You can use the scripts as a starting point for your own implementation.

Although both approaches achieve the same goal, I personally recommend the threading approach because it is easier to implement.
Specifically, once you have a sync implementation, you can easily convert it to a threading implementation without much effort.
But turning the sync implementation to async requires a lot of changes.
Below I provide a detailed explanation of the two approaches and you can see the differences clearly.

## Warning

Async programming and threading can be complicated, and you might run into all sorts of issues if you don't know what you are doing.
My suggestion is that you should only consider this approach when you absolutely need it.
If you don't have that many text messages to process, you can just use a for loop.
If you are not in a rush, you should also consider the new [batch API](/batch_processing), which is much easier to handle and costs only half the price.

# Detailed explanation

Here I provide a detailed explanation of the two approaches.

First, let's define the text messages and the prompt.
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
The prompt would be the same as the examples in other topics.

### Sync implementation
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

### Threading implementation

Now, let's use threading to process the text messages.
We can reuse the sync function above and wrap it in a `thread_map` function from the `concurrent.futures` module.

Note that we define a `N_THREADS` variable to set the number of threads.
Increasing the number of threads will speed up the processing, but it will also increase the memory usage.
And the marginal improvement will decrease as the number of threads increases.

```python
from concurrent.futures import ThreadPoolExecutor

N_THREADS = 3
print(f"Threading method with {N_THREADS} threads:")
start_time = time.perf_counter()
with ThreadPoolExecutor(max_workers=N_THREADS) as executor:
    threading_results = list(executor.map(process_text_message, text_messages))
end_time = time.perf_counter()
print(f"Threading method done in {end_time - start_time:.2f} seconds.")
for result in threading_results:
    print(result)
```

See [compare_sync_threading.py](/async_programming/compare_sync_threading.py) for the full code and comparison between the sync and threading versions.

### Async implementation

Now, let's try the async version.
First, we need to define an async function to query the API:
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
See [compare_sync_async.py](/async_programming/compare_sync_async.py) for the full code and comparison between the sync and async versions.

## Template scripts

To help you get started, I create two template scripts:
- [async template script](/async_programming/async_template.py)
- [threading template script](/async_programming/threading_template.py)

Both of them have some other nice features, like setting a timeout for each request and using tqdm to show the progress.
You might still need to add more code to handle other errors to make your application more robust, though.