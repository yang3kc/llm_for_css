# Introduction

Here, we introduce how to get structured output from OpenAI's API, which is extremely handy if you have to process large amounts of data programmatically.

# Structured output

Many LLMs providers support structured output now, which would produce structured output that's easy for programs to parse.
Here, we will focus on [OpenAI's API](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses).

Let's modify our basic script for sentiment analysis and demonstrate the use of structured output.

There are two things we need to do.
First, we need to modify the prompt to instruct the model to return the output in JSON format and specify the schema.

```python
text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"""
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    """
```

Second, we need to define the schema of the output in the prompt.

```python
from pydantic import BaseModel, Field

class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive."
    )
    explanation: str = Field(description="Explanation of the sentiment score.")
```


Now we are ready to query the API.

```python
response = client.responses.parse(
    model="gpt-4.1-mini",
    temperature=0.0,
    instructions=system_prompt,
    input=user_instruction,
    text_format=Sentiment,
)
```

The output of the response will be automatically parsed into the Pydantic model we defined.
You can access the parsed output by calling `response.output_parsed`.

The whole script can be found in [structured_output.py](/structured_output/structured_output.py)

Alternatively, you can also use the JSON schema to get the output as a string and parse it yourself.

The whole script can be found in [structured_output_schema.py](/structured_output/structured_output_schema.py)

# Additional tips

If you are using the API from a provider that doesn't support structured output, you can still use the JSON mode to get a JSON string and parse it yourself.

A particular useful tool I found is [`json_repair`](https://github.com/mangiucugna/json_repair), which can repair invalid JSON strings.

With a valid JSON string, you could do so by using the `json` module in Python to parse the output and check each field in the schema yourself.
But I suggest using [pydantic](https://docs.pydantic.dev/latest) for this purpose.