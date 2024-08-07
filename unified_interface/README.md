# Introduction

In this folder, I provide a unified interface for querying different models.
Currently, it only supports models from OpenAI (the GPT models), Google (the Gemini models), and Together.ai (various open-source models).
But, it shouldn't be too difficult to extend it to other providers.

To use the unified interface, you need to install the dependencies first.

- `openai`
- `google-generativeai`
- `together`

You will also need to obtain the API keys for these providers.

# Explanation of the code

In `api_factory.py`, I define a set of classes to support different providers and a function `create_api_client` to create a client for a given provider.

Now you can use the same interface to query different models from different providers.

```python
# First, choose a provider and a model
provider = "openai"
model = "gpt-4o"

# provider = "google"
# model = "gemini-1.5-flash"

# provider = "together"
# model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

# Then, create a client for the chosen provider
api_client = api_factory.create_api_client(provider, api_key)
result = api_client.query_model(model, system_prompt, user_instruction)
```

In `query_llm.py`, I demonstrate how to query a LLM using a unified interface.

# Caveats

Different models within each provider might have different parameters, so you need to go to `api_factory.py` to change those parameters directly.

I haven't tested querying those APIs asynchronously, so you might need to figure it out yourself.