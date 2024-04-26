# Introduction

Using LLMs for computational social science research can be as simple as asking the models questions in plain text and expecting responses.
However, things can become tricky when you want to use the model to process tens of thousands of text messages programmatically.

The goal of this repository is to provide guidance, recommendations, and examples on how to do this correctly and efficiently.
I'll focus on OpenAI's API.
But many of the tips and tricks are applicable to other providers as well.
The following topics are covered:

1. [Handling API keys properly](#api-key)
1. [Writing a simple Python script to query the API](#simple-python-script-to-query-the-api)
1. Using JSON mode to obtain structured output and parse (validate) the output
1. Using async programming to accelerate the querying process
1. Using the batch API to process large amounts of data with reduced cost

# API key

Fist rule of working with API providers: **Never** put your API key in your script or Jupyter notebook.
In other words, you should **not** start your script with the following:

```python
from openai import OpenAI

client = OpenAI(api_key="<your OpenAI API key>")
```

Instead, consider adding the API key as an environment variable called `OPENAI_API_KEY`, which can be achieved with the following shall command:

```bash
export OPENAI_API_KEY="<your OpenAI API key>"
```
You can also add this to your `.bashrc` or `.zshrc` file for convenience.

Then, you can start your script or Jupyter notebook with the following:

```python
from openai import OpenAI

client = OpenAI()
```

The `openai` package will automatically use the API key from the environment variable `OPENAI_API_KEY`.

Alternatively, you can consider using the [`python-dotevn`](https://github.com/theskumar/python-dotenv) package to load the API key from the `.env` file.
Remember to add `.env` to your `.gitignore` file to prevent it from being committed.

# Simple Python script to query the API

Let's start with a simple example to query the OpenAI API.

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

This is pretty good!

But in computational social science research, we typically have thousands of text messages to process.
And using the simple script above becomes difficult for a couple of reasons:
1. The output is in plain text.
Although it's easy for human to extract the key information, dealing with it using programs is difficult.
2. Running the script to process your text messages one by one can be slow.

To deal with issue 1, we can leverage the JSON mode of OpenAI's API to force the output format.
See [structured_output](/structured_output) for details.

For issue 2, there are two options:
1. If you need the results immediately, you can consider using the async programming to accelerate the querying process. See [async_programming](/async_programming) for details.
1. If you can wait, you can use the batch API to process large amounts of data with reduced cost. See [batch_processing](/batch_processing) for details.