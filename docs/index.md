# LLM for Computational Social Science

Using LLMs for computational social science research can be as simple as asking the models questions through a chat box and expecting responses.
However, things become tricky when you want to use the model to process tens of thousands of text messages programmatically.

The goal of this website is to provide guidance, recommendations, and examples on how to do this correctly and efficiently.
The core chapters use OpenAI's API.
The later chapters show the same patterns with Anthropic, hosted open-source models, and models running on your own computer.
The following topics are covered:

1. [Handling API keys properly](#api-key-please-read-this-first) (on this page)
1. [Writing a simple Python script to query the API](basics.ipynb)
1. [Obtaining structured output](structured_output.ipynb)
1. [Using async programming to accelerate the querying process](async_programming.ipynb)
1. [Using the batch API to process large amounts of data with reduced cost](batch_processing.md)
1. [Using Anthropic's Claude models](anthropic.ipynb)
1. [Using open-source models via hosted APIs](open_source_models.ipynb)
1. [Running LLMs locally](local_llms.md)

Most sections are runnable Jupyter notebooks — use the **Open in Colab** badge at the top of a page to try the code without installing anything. The notebooks and remaining scripts live in the [GitHub repository](https://github.com/yang3kc/llm_for_css).

## Which provider should I use?

The tutorial covers four ways to reach a model.
The code is nearly the same for all of them: the `openai` Python package works with every provider except Anthropic, and Anthropic's package follows the same shape.
Prices are per 1M tokens (input / output) for the example model each chapter uses, as of September 2026; check the provider's pricing page before a large run.

| Provider | Example model | Price per 1M tokens | Setup | Pick it when |
|---|---|---|---|---|
| [OpenAI](basics.ipynb) | `gpt-5.6-luna` | $0.20 / $1.20 | One account and key | You are starting out. Most capable ecosystem, best documentation, and the [batch API](batch_processing.md) halves the price for large jobs. |
| [Anthropic](anthropic.ipynb) | `claude-haiku-4-5` | $1 / $5 | One account and key | You want a second model family to check robustness, or Claude works better on your task. Also has a 50% batch discount. |
| [Open-source models via OpenRouter](open_source_models.ipynb) | `deepseek/deepseek-v4-flash` | $0.08 / $0.15 | One account and key | You want the lowest per-token cost, access to many open-weight models through one key, or a model you can name exactly in a paper. |
| [Local with Ollama](local_llms.md) | `gemma4:e2b` | Free | Install Ollama, download a 7 GB model | Your data cannot leave your machine, or you need to rerun the same model years later. Slower and less capable than the hosted options. |

A practical default: prototype the prompt on a few hundred examples with OpenAI, then decide.
If the task is easy for the model, switch to the cheapest option that still passes your validation set.
If the data is sensitive, start with the local chapter instead.

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

All the topics on the original roadmap (other API providers, open-source models, running LLMs locally) are now covered.

If you have questions or suggestions, please [open issues](https://github.com/yang3kc/llm_for_css/issues).
Pull requests are also welcome!

## Other resources

Find this website useful? Check out my other repos!

- [daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest): Using ChatGPT to select interesting arXiv papers
- [cursor_latex_template](https://github.com/yang3kc/cursor_latex_template): Cursor configuration for LaTeX projects
- [llm_git_commit](https://github.com/yang3kc/llm_git_commit): Command line tool to use LLM to generate git commit messages
