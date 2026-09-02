# LLM for Computational Social Science

<p class="lead" markdown>
Guidance, recommendations, and runnable examples for using LLM APIs in computational social science research: from a first API call to processing tens of thousands of text messages efficiently and at low cost.
</p>

Using LLMs for research can be as simple as asking the models questions through a chat box.
Things become tricky when you want to process tens of thousands of text messages programmatically: keeping keys safe, getting output you can parse, running queries in parallel, and controlling cost.
This website walks through each of those steps.

!!! note "What this site does not cover"
    This is a technical guide to interacting with LLMs from code.
    It does not explain how LLMs work, and it is not about AI agents.
    It also does not cover the methodological side of using LLMs in research, such as validating model output against human labels or reporting results.
    Those questions matter, but they belong elsewhere.
The core chapters use OpenAI's API.
The later chapters show the same patterns with Anthropic, hosted open-source models, and models running on your own computer.

Most chapters are runnable Jupyter notebooks.
Use the **Open in Colab** badge at the top of a page to try the code without installing anything.
The notebooks and scripts live in the [GitHub repository](https://github.com/yang3kc/llm_for_css).

## Start here

Read the [API key](#api-key-please-read-this-first) section below first, then go through the OpenAI chapters in order.

<div class="grid cards" markdown>

-   :material-play-circle-outline:{ .lg .middle } **Basics**

    ---

    Your first API call from Python: set up the client, send a prompt, read the response.

    [:octicons-arrow-right-24: Basics](basics.ipynb)

-   :material-code-json:{ .lg .middle } **Structured output**

    ---

    Get answers back as validated Python objects instead of free text.

    [:octicons-arrow-right-24: Structured output](structured_output.ipynb)

-   :material-fast-forward-outline:{ .lg .middle } **Async programming**

    ---

    Send many requests at once so a large dataset takes minutes, not hours.

    [:octicons-arrow-right-24: Async programming](async_programming.ipynb)

-   :material-package-variant-closed:{ .lg .middle } **Batch processing**

    ---

    Upload all your prompts in one file and pay half price for large jobs.

    [:octicons-arrow-right-24: Batch processing](batch_processing.md)

</div>

## Other providers

The same patterns work beyond OpenAI.
Each chapter covers setup, a basic query, and structured output.

<div class="grid cards" markdown>

-   :material-alpha-a-box-outline:{ .lg .middle } **Anthropic API**

    ---

    Claude models through Anthropic's Python package.

    [:octicons-arrow-right-24: Anthropic API](anthropic.ipynb)

-   :material-cloud-outline:{ .lg .middle } **Open-source models**

    ---

    Open-weight models through a hosted API (OpenRouter), using the same `openai` package.

    [:octicons-arrow-right-24: Open-source models](open_source_models.ipynb)

-   :material-laptop:{ .lg .middle } **Local LLMs**

    ---

    Run a model on your own computer with Ollama: no key, no per-token cost, data stays local.

    [:octicons-arrow-right-24: Local LLMs](local_llms.md)

</div>

## Which provider should I use?

The tutorial covers four ways to reach a model.
The code is nearly the same for all of them: the `openai` Python package works with every provider except Anthropic, and Anthropic's package follows the same shape.
Prices are per 1M tokens (input / output) for the example model each chapter uses, as of September 2026; check the provider's pricing page before a large run.

| Provider | Example model | Price per 1M tokens | Setup | Pick it when |
|---|---|---|---|---|
| [OpenAI](basics.ipynb) | `gpt-5.6-luna` | $0.20 / $1.20 | One account and key | You are starting out. Most capable ecosystem, best documentation, and the [batch API](batch_processing.md) halves the price for large jobs. |
| [Anthropic](anthropic.ipynb) | `claude-haiku-4-5` | $1 / $5 | One account and key | You want a second model family to check robustness, or Claude works better on your task. Also has a 50% batch discount. |
| [Open-source models via OpenRouter](open_source_models.ipynb) | `deepseek/deepseek-v4-flash` | $0.08 / $0.15 | One account and key | You want the lowest per-token cost, access to many open-weight models through one key, or a model you can name exactly in a paper. |
| [Local with Ollama](local_llms.md) | `gemma4:e2b` | Free | Install Ollama, download a 7 GB model | Your data cannot leave your machine, or you need to rerun the same model years later. Slower and less capable than the hosted options on a laptop; a [GPU workstation](local_llms.md#on-a-gpu-workstation) runs 100B-class models. |

A practical default: prototype the prompt on a few hundred examples with OpenAI, then decide.
If the task is easy for the model, switch to the cheapest option that still passes your validation set.
If the data is sensitive, start with the local chapter instead.

## API key: read this first { #api-key-please-read-this-first }

First rule of working with API providers: **never** put your API key in your script or Jupyter notebook.
In other words, do **not** start your script with the following:

```python
from openai import OpenAI

client = OpenAI(api_key="<your OpenAI API key>")
```

Instead, add the API key as an environment variable called `OPENAI_API_KEY`:

```bash
export OPENAI_API_KEY="<your OpenAI API key>"
```

You can add this line to your `.bashrc` or `.zshrc` file for convenience.
Then start your script or Jupyter notebook with:

```python
from openai import OpenAI

client = OpenAI()
```

The `openai` package reads the key from the `OPENAI_API_KEY` environment variable automatically.

Alternatively, use the [`python-dotenv`](https://github.com/theskumar/python-dotenv) package to load the key from a `.env` file.
Remember to add `.env` to your `.gitignore` file so it is never committed.
See [.env.template](https://github.com/yang3kc/llm_for_css/blob/main/.env.template) for an example.

!!! tip "On Google Colab"
    Use Colab Secrets instead: click the key icon in the left sidebar, add a secret named `OPENAI_API_KEY`, and enable notebook access.
    The tutorial notebooks read the key from there automatically.

## Dependencies

We use [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies for this project.
To install them, clone the [repository](https://github.com/yang3kc/llm_for_css) and run:

```bash
uv sync
```

Run a script with:

```bash
uv run script.py
```

## Questions and contributions

If you have questions or suggestions, please [open an issue](https://github.com/yang3kc/llm_for_css/issues).
Pull requests are also welcome.

## Other resources

Find this website useful? Check out my other repos:

- [daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest): Using ChatGPT to select interesting arXiv papers
- [cursor_latex_template](https://github.com/yang3kc/cursor_latex_template): Cursor configuration for LaTeX projects
- [llm_git_commit](https://github.com/yang3kc/llm_git_commit): Command line tool to use LLM to generate git commit messages
