# LLM for Computational Social Science

Using LLMs for computational social science research can be as simple as asking the models questions through a chat box and expecting responses.
However, things become tricky when you want to use the model to process tens of thousands of text messages programmatically.

The goal of this website is to provide guidance, recommendations, and examples on how to do this correctly and efficiently.
I'll focus on OpenAI's API.
But many of the tips and tricks are applicable to other providers as well.
The following topics are covered:

1. [Handling API keys properly](#api-key-please-read-this-first) (on this page)
1. [Writing a simple Python script to query the API](basics.ipynb)
1. [Obtaining structured output](structured_output.ipynb)
1. [Using async programming to accelerate the querying process](async_programming.ipynb)
1. [Using the batch API to process large amounts of data with reduced cost](batch_processing.md)
1. [Using Anthropic's Claude models](anthropic.ipynb)

Chapters on open-source models via hosted APIs and running LLMs locally are planned.

Most sections are runnable Jupyter notebooks — use the **Open in Colab** badge at the top of a page to try the code without installing anything. The notebooks and remaining scripts live in the [GitHub repository](https://github.com/yang3kc/llm_for_css).

## API key (please read this first!!!)

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

See [.env.template](https://github.com/yang3kc/llm_for_css/blob/main/.env.template) for an example of the `.env` file.

On **Google Colab**, use Colab Secrets instead: click the key icon in the left sidebar, add a secret named `OPENAI_API_KEY`, and enable notebook access. The tutorial notebooks read the key from there automatically.

## Dependencies

We use [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies for this project.

To install the dependencies, clone the [repository](https://github.com/yang3kc/llm_for_css) and run the following command:

```bash
uv sync
```

You can run the scripts using the following command:

```bash
uv run script.py
```

## Roadmap

I'm also considering writing on the following topics:

1. Querying other API providers, such as closed-source model providers like Google and Anthropic and open-source model providers.
1. Running LLMs locally.

If you have questions or suggestions, please [open issues](https://github.com/yang3kc/llm_for_css/issues).
Pull requests are also welcome!

## Other resources

Find this website useful? Check out my other repos!

- [daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest): Using ChatGPT to select interesting arXiv papers
- [cursor_latex_template](https://github.com/yang3kc/cursor_latex_template): Cursor configuration for LaTeX projects
- [llm_git_commit](https://github.com/yang3kc/llm_git_commit): Command line tool to use LLM to generate git commit messages
