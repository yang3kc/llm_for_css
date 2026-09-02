# LLM for Computational Social Science

Guidance, recommendations, and runnable examples for using LLM APIs in computational social science research: from a first API call to processing tens of thousands of text messages efficiently and at low cost.

**Read the tutorial on the website: https://yang3kc.github.io/llm_for_css/**

The website is the canonical version of the tutorial.
This repository holds its source: the notebooks and scripts, and the MkDocs configuration that builds the site.

## What is covered

| Chapter | Format |
|---|---|
| [Basics](https://yang3kc.github.io/llm_for_css/basics/): your first API call from Python | Notebook |
| [Structured output](https://yang3kc.github.io/llm_for_css/structured_output/): answers as validated Python objects | Notebook |
| [Async programming](https://yang3kc.github.io/llm_for_css/async_programming/): many requests at once | Notebook + template scripts |
| [Batch processing](https://yang3kc.github.io/llm_for_css/batch_processing/): half price for large jobs | Notebook |
| [Anthropic API](https://yang3kc.github.io/llm_for_css/anthropic/): Claude models | Notebook |
| [Open-source models](https://yang3kc.github.io/llm_for_css/open_source_models/): open-weight models through OpenRouter | Notebook |
| [Local LLMs](https://yang3kc.github.io/llm_for_css/local_llms/): run a model on your own computer with Ollama | Scripts |

Not sure where to start? See [Which provider should I use?](https://yang3kc.github.io/llm_for_css/#which-provider-should-i-use) on the website.

Every notebook has an **Open in Colab** badge, so you can run it without installing anything.

## Running the code locally

1. Clone the repository and install the dependencies with [uv](https://docs.astral.sh/uv/getting-started/installation/):

   ```bash
   uv sync
   ```

2. Set your API key. **Never put the key in a script or notebook.** Either export it as an environment variable:

   ```bash
   export OPENAI_API_KEY="<your OpenAI API key>"
   ```

   or copy [`.env.template`](.env.template) to `.env` and fill it in (`.env` is git-ignored). The [API key section](https://yang3kc.github.io/llm_for_css/api_key/) on the website has the details, including how to do this on Colab.

3. Run a script, for example:

   ```bash
   uv run async_programming/async_template.py
   ```

   or open a notebook from `docs/` in Jupyter.

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | The website pages: the notebooks (`*.ipynb`) and the markdown chapters |
| `async_programming/`, `batch_processing/`, `local_llms/` | Scripts and data files that the chapters embed or link to |
| `basics/`, `structured_output/` | Pointer READMEs kept for old links; the content moved to notebooks in `docs/` |
| `mkdocs.yml` | Site configuration (Material for MkDocs) |
| `.env.template` | Template for the local `.env` file |

To preview the website locally:

```bash
uv sync --group docs
uv run mkdocs serve
```

The site is deployed to GitHub Pages by a GitHub Actions workflow on every push to `main`.

## Versions

- **v2.0 (current):** Responses API, structured output via the text format method, dependencies managed with uv, notebooks as the canonical format, and chapters for Anthropic, open-source models, and local LLMs.
- **v1.0:** Chat Completions API. Still available on the [v1.0 branch](https://github.com/yang3kc/llm_for_css/tree/v1.0).

## Questions and contributions

If you have questions or suggestions, please [open an issue](https://github.com/yang3kc/llm_for_css/issues).
Pull requests are also welcome.

## Other resources

Find this repository useful? Check out my other repos:

- [daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest): Using ChatGPT to select interesting arXiv papers
- [cursor_latex_template](https://github.com/yang3kc/cursor_latex_template): Cursor configuration for LaTeX projects
- [llm_git_commit](https://github.com/yang3kc/llm_git_commit): Command line tool to use LLM to generate git commit messages
