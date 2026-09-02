# API key: read this first

**Never** put your API key in your script or Jupyter notebook. Do **not** start your script with the following:

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
Add `.env` to your `.gitignore` file so it is never committed.
See [.env.template](https://github.com/yang3kc/llm_for_css/blob/main/.env.template) for an example.

!!! tip "On Google Colab"
    Use Colab Secrets instead: click the key icon in the left sidebar, add a secret named `OPENAI_API_KEY`, and enable notebook access.
    The tutorial notebooks read the key from there automatically.
