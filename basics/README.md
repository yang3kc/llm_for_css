# Introduction

Let's start with a simple example to query the OpenAI API.
All the other more complex examples will be based on this one.

# Example on sentiment analysis

Considering the following sentiment analysis tasks.
We have some text messages and we want to know if it is positive or negative.
One way to do this is to ask ChatGPT to produce binary labels.
But to get the nuanced results, we can let it generate a score in the range of -1 to 1, where -1 means negative and 1 means positive.
Here is the code

```python
from openai import OpenAI

text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."
user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    temperature=0,
    instructions=system_prompt,
    input=user_instruction,
)

print(response.output_text)
```

You can see and run the [script](/basics/senti_basic.py) directly with the following command:

```bash
uv run senti_basic.py
```

The output I got is (note that the response might be different for you even though the temperature is set to 0):

```
The sentiment score for the text message "The service here is very good!" is **0.8**.

Explanation: The phrase "very good" clearly indicates a positive sentiment towards the service. The use of "very" intensifies the positivity, making it stronger than just "good." There are no negative words or mixed sentiments present. However, since it is a straightforward positive statement without extreme enthusiasm or superlatives like "excellent" or "amazing," the score is high but not at the maximum of 1.
```

# Next steps

The script above is very simple and effective.
But in computational social science research, we often have tens of thousands of text messages to process.
And using the simple script above becomes difficult for a couple of reasons:
1. The output is in plain text.
Although it's easy for human to extract the key information, dealing with it using programs is difficult.
2. Running the script to process your text messages one by one can be slow.

To deal with issue 1, we can leverage the structured output of OpenAI's API to specify the output format.
See [structured_output](/structured_output) for details.

For issue 2, there are two options:
1. If you need the results immediately, you can consider using the async programming to accelerate the querying process. See [async_programming](/async_programming) for details.
1. If you are not in a rush, you can use the batch API to process large amounts of data with reduced cost. See [batch_processing](/batch_processing) for details.

Personally, I prefer the second option because it can significantly reduce the cost and doesn't need to deal with the async programming.
Some other providers such as Anthropic also provide batch API, but others still don't.