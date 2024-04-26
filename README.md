# Introduction

Using LLMs for computational social science research can be as simple as asking the models questions in plain text and expecting responses.
However, things can become tricky when you want to use the model to process tens of thousands of text messages programmatically.

The goal of this repository is to provide guidance, recommendations, and examples on how to do this correctly and efficiently.
I'll focus on OpenAI's API.
But many of the tips and tricks are applicable to other providers as well.
The following topics are covered:

1. Handling API keys properly
1. Writing a simple Python script to query the API
1. Using JSON mode to obtain structured output and parse (validate) the output
1. Using async programming to accelerate the querying process
1. Using the batch API to process large amounts of data with reduced cost

# API key

Fist rule of working with API providers: **Never** put your API key in your script or Jupyter notebook.
In other words, you should **not** start your script with the following:

```python
import OpenAI

client = OpenAI(api_key="<your OpenAI API key>")
```

Instead, consider adding the API key as an environment variable called `OPENAI_API_KEY`, which can be achieved with the following shall command:

```bash
export OPENAI_API_KEY="<your OpenAI API key>"
```
You can also add this to your `.bashrc` or `.zshrc` file for convenience.

Then, you can start your script or Jupyter notebook with the following:

```python
import OpenAI

client = OpenAI()
```

The `openai` package will automatically use the API key from the environment variable `OPENAI_API_KEY`.

Alternatively, you can consider using the [`python-dotevn`](https://github.com/theskumar/python-dotenv) package to load the API key from the `.env` file.
Remember to add `.env` to your `.gitignore` file to prevent it from being committed.