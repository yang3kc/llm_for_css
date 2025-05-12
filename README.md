# Introduction

## Change logs
**[v2.0 changes]**:
- Moved from OpenAI's Chat Completions API to Responses API.
- Using the text format method to define structured output.
- Using [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies.

If you still need to use the Chat Completions API, check out the [v1.0 branch](https://github.com/yang3kc/llm_for_css/tree/v1.0).

## Background

Using LLMs for computational social science research can be as simple as asking the models questions through a chat box and expecting responses.
However, things become tricky when you want to use the model to process tens of thousands of text messages programmatically.

The goal of this repository is to provide guidance, recommendations, and examples on how to do this correctly and efficiently.
I'll focus on OpenAI's API.
But many of the tips and tricks are applicable to other providers as well.
The following topics are covered:

1. [Handling API keys properly](#api-key-please-read-this-first)
1. [Writing a simple Python script to query the API](/basics) (TODO)
1. [Using JSON mode to obtain structured output and parse (validate) the output](/structured_output) (TODO)
1. [Using async programming to accelerate the querying process](/async_programming) (TODO)
1. [Using the batch API to process large amounts of data with reduced cost](/batch_processing) (TODO)
1. [Querying different models in a unified interface](/unified_interface) (TODO)

# API key (please read this first!!!)

First rule of working with API providers: **Never** put your API key in your script or Jupyter notebook.
In other words, you should **not** start your script with the following:

```python
from openai import OpenAI

client = OpenAI(api_key="<your OpenAI API key>")
```

Instead, consider adding the API key as an environment variable called `OPENAI_API_KEY`, which can be achieved with the following shell command:

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

Alternatively, you can consider using the [`python-dotenv`](https://github.com/theskumar/python-dotenv) package to load the API key from the `.env` file.
Remember to add `.env` to your `.gitignore` file to prevent it from being committed.

See [.env.example](.env.example) for an example of the `.env` file.


# Dependencies

We use [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies for this project.

To install the dependencies, run the following command:

```bash
uv sync
```

# Roadmap

I'm also considering writing on the following topics:
1. Querying other API providers, such as closed-source model providers like Google and Anthropic and open-source model providers.
1. Running LLMs locally.

If you have questions or suggestions, please open issues.
Pull requests are also welcome!
