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

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.0,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
)

print(completion.choices[0].message.content)
```

You can see and run the [script](/basics/senti_basic.py) directly.

The output is

```
Sentiment Score: 0.8

Explanation: The text message "The service here is very good!" conveys a positive sentiment. The use of the word "good" and the intensifier "very" both indicate a high level of satisfaction with the service. Overall, the message expresses a positive sentiment towards the service, hence the score of 0.8.
```

# Next steps

The script above is very simple and effective.
But in computational social science research, we often have tens of thousands of text messages to process.
And using the simple script above becomes difficult for a couple of reasons:
1. The output is in plain text.
Although it's easy for human to extract the key information, dealing with it using programs is difficult.
2. Running the script to process your text messages one by one can be slow.

To deal with issue 1, we can leverage the JSON mode of OpenAI's API to specify the output format.
See [structured_output](/structured_output) for details.

For issue 2, there are two options:
1. If you need the results immediately, you can consider using the async programming to accelerate the querying process. See [async_programming](/async_programming) for details.
1. If you are not in a rush, you can use the batch API to process large amounts of data with reduced cost. See [batch_processing](/batch_processing) for details.

Personally, I prefer the second option because it can significantly reduce the cost and doesn't need to deal with the async programming.
But only OpenAI offers batch API right now, while async programming works well with other providers too.