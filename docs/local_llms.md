# Running LLMs locally

The previous chapters all sent your data to a server somewhere else: OpenAI, Anthropic, or a hosting provider behind OpenRouter.
This chapter runs an open-weight model on your own computer instead.
For computational social science research, this brings three benefits:

1. **Privacy**: your data never leaves your machine. This matters when you work with sensitive data, or when your IRB protocol or data agreement forbids sending the data to a third party.
2. **No per-token cost**: once the model is downloaded, you can run as many queries as you want. The only cost is your electricity and your time.
3. **Reproducibility**: the model file sits on your disk. Nobody can deprecate it or update it under you, so you can name the exact version in your paper and rerun the analysis years later.

The trade-off is capability and speed.
A model that fits on a laptop is much smaller than the models behind the commercial APIs, so it is less capable, and your laptop is much slower than a data center.
For many classification and extraction tasks in social science, a small local model is good enough.
For harder tasks, test on a sample before you commit.

This chapter uses [Ollama](https://ollama.com/), a free, open-source tool that downloads models and serves them behind an API on your machine.
Its API is compatible with OpenAI's SDK, so the code is nearly identical to the [open-source models](open_source_models.ipynb) chapter.

This chapter has no Colab notebook, because Colab cannot easily host a local model server.
The scripts are in the [`local_llms/`](https://github.com/yang3kc/llm_for_css/tree/main/local_llms) folder of the repository, and you run them on your own computer.

## Setup

### Install Ollama

Download the installer for macOS, Windows, or Linux from the [Ollama download page](https://ollama.com/download).
On macOS, you can also install it with Homebrew:

```bash
brew install ollama
```

The desktop app starts the server automatically.
If you installed with Homebrew, start it yourself in a terminal:

```bash
ollama serve
```

Leave that terminal open while you work.
The server listens on `http://localhost:11434`.

### Download a model

Ollama hosts a [library of open-weight models](https://ollama.com/search).
We use `gemma4:e2b` in this chapter, a small model from Google's Gemma 4 family that is designed for consumer hardware.
Download it with:

```bash
ollama pull gemma4:e2b
```

The download is about 7 GB and only happens once.
To check that everything works, chat with the model from the terminal (type `/bye` to exit):

```bash
ollama run gemma4:e2b
```

!!! tip "Choosing a model"
    The rule of thumb is that a model needs slightly more memory than its file size.
    `gemma4:e2b` uses about 7 GB of memory when loaded, so it runs on a machine with 16 GB of RAM and leaves room for your other programs.
    On a machine with 8 GB, try the more compressed `gemma4:e2b-it-qat` tag (4.3 GB).
    If you have a workstation with a large GPU or a Mac with 64 GB or more, larger models such as `gemma4:26b` or `qwen3.6:27b` are more capable.
    Browse the [model library](https://ollama.com/search) for other options; every model page lists its sizes.

### Install the Python package

There is no key to configure, because there is no account.
The Python dependencies are the `openai` and `pydantic` packages, the same as in the earlier chapters.
If you cloned this repository, `uv sync` already installed them.
In your own project, add them with:

```bash
uv add openai pydantic
```

## Basic query

Let's run the same sentiment analysis example against the local model.
Compared to the [open-source models](open_source_models.ipynb) chapter, there are two changes:

1. `base_url` points at the Ollama server on your machine, and `api_key` can be any string. The SDK requires a key, but Ollama ignores it.
2. `gemma4:e2b` is a "thinking" model, meaning it writes out a chain of reasoning before answering. That is useful for hard problems, but for a short classification task it makes each query many times slower. Set `reasoning_effort="none"` to turn it off.

```python
--8<-- "local_llms/basic_query.py"
```

Running the script gives:

```
**Sentiment Score:** 1.0

**Explanation:**

The text message "The service here is very good!" uses a strongly positive adjective ("very good") to describe the service. This clearly indicates a positive feeling or satisfaction from the sender regarding the service. Therefore, the sentiment is overwhelmingly positive, resulting in a score of 1.0.
```

On an Apple M4 Max laptop, this query takes under one second.
The first query after starting the server takes longer, because Ollama loads the model into memory.
It stays loaded for five minutes after the last request, then unloads to free the memory.

## Structured output

Structured output works the same way as before.
The `client.chat.completions.parse` method takes the Pydantic model in `response_format`, and Ollama constrains the model's output to match the schema.

```python
--8<-- "local_llms/structured_output.py"
```

Running the script gives:

```
{'score': 1.0, 'explanation': "The text 'The service here is very good!' uses the positive adjective 'good' and an intensifier 'very'. This clearly expresses a positive opinion about the service, resulting in a strongly positive sentiment."}
Score: 1.0
Explanation: The text 'The service here is very good!' uses the positive adjective 'good' and an intensifier 'very'. This clearly expresses a positive opinion about the service, resulting in a strongly positive sentiment.
```

## Scaling up

The async and threading templates from the [async programming](async_programming.ipynb) chapter work unchanged: use `AsyncOpenAI` with the same `base_url` and `api_key`.
There is one important difference from the hosted APIs.
Ollama processes one request at a time per model by default, so sending 20 concurrent requests will not make things faster; they queue on your machine.
You can raise the limit with the `OLLAMA_NUM_PARALLEL` environment variable before starting the server, but the total throughput is bounded by your hardware either way.
For a dataset of tens of thousands of messages, a plain loop that runs overnight is often the practical answer.

There is no batch API, because there is no server to hand the work to.
If you need higher throughput, the options are a machine with a bigger GPU, or a hosted provider from the [open-source models](open_source_models.ipynb) chapter running the same model.

## Other ways to run models locally

Ollama is the easiest starting point, but it is not the only option.

- [llama.cpp](https://github.com/ggml-org/llama.cpp) is the inference engine underneath Ollama. Using it directly gives you more control over quantization and hardware settings, at the cost of more setup. Its `llama-server` also exposes an OpenAI-compatible API.
- [LM Studio](https://lmstudio.ai/) is a desktop app with a graphical interface for downloading and chatting with models. It can also serve an OpenAI-compatible API, so the code in this chapter works with it after changing the port.
- [vLLM](https://docs.vllm.ai/) is built for serving many parallel requests on server GPUs. If your university gives you access to a GPU cluster, this is the tool for processing a large dataset quickly.

All of them serve an OpenAI-compatible API, so what you learned here transfers.
