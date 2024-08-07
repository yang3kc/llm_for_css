# Introduction

Here, we introduce how to get structured output from OpenAI's API, which is extremely handy if you have to process large amounts of data programmatically.

# JSON mode

Many LLMs providers support JSON mode, which would produce structured output that's easy for programs to parse.
Here, we will show how to use [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode) for OpenAI's API.

**Note:** OpenAI recently announced a new ["structured output" feature](https://openai.com/index/introducing-structured-outputs-in-the-api) that can further guarantee the output is in the JSON format.

Let's modify our basic script for sentiment analysis and demonstrate the use of JSON mode.

There are two things we need to do.
First, we need to modify the prompt to instruct the model to return the output in JSON format and specify the schema.

```python
text_message = "The service here is very good!"

system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."

user_instruction = f"""
    Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive.
    Also explain why.
    The output should be in JSON format and follow the following schema:
    --------------
    ```json
    {{
        'score': 0.1,
        'explanation': '...'
    }}
     ```
    """
```

You can see that I added additional instructions on the output format to the `user_instruction`, which should be self-explanatory.

Second, we need to turn on the JSON mode in the API call by adding the `response_format` parameter:

```python
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.0,
    # Remember to turn the JSON mode on
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ],
)
```

The output now looks like this:
```json
{
    "score":0.9,
    "explanation": "The text message 'The service here is very good!' expresses a positive sentiment with the use of words like 'good' and 'very'. Therefore, the sentiment score is closer to 1, indicating a highly positive sentiment."
}
```
which is exactly what we wanted.

# Output validation

Even with the JSON model, LLMs can still return invalid outputs, this is why we need to further process and validate the output.

A particular useful tool I found is [`json_repair`](https://github.com/mangiucugna/json_repair), which can repair invalid JSON strings.

With a valid JSON string, you could do so by using the `json` module in Python to parse the output and check each field in the schema yourself.
But I suggest using [pydantic](https://docs.pydantic.dev/latest) for this purpose.

In the sentiment analysis, we can define a Pydantic model to validate the output:
```python
from pydantic import BaseModel, Field

class Sentiment(BaseModel):
    score: float = Field(
        description="Sentiment score in the range of -1 to 1, where -1 means negative and 1 means positive.",
        ge=-1,
        le=1,
    )
    explanation: str = Field(description="Explanation of the sentiment score.")
```

The data model should be consistent with the schema defined in the prompt.

Now we can validate the output:
```python
senti_score_result = Sentiment.model_validate_json(
    completion.choices[0].message.content
)
```
If the output is invalid, an error will be raised.
The situations might include:
1. The output is not in JSON format.
1. Score is not in the range of -1 to 1.
1. The output is not in the schema defined in the prompt.

In such cases, you could try to query the API again and will likely get a valid output.

For valid output, you can print the result as a dictionary:
```python
senti_score_dict = senti_score_result.model_dump()
print(senti_score_dict)
```

You can also obtain the JSON string if you want to store it in a file:

```python
senti_score_json = senti_score_result.model_dump_json()
```

The whole script can be found in [json_mode.py](/structured_output/json_mode.py)

# Next steps

In this tutorial, I try to keep things simple and avoid using advanced prompt engineering tools.
But they can be handy if the simple solution here doesn't fit your use case.
I won't go into the details, but below are some tools that are worth checking out:

- [instructor](https://python.useinstructor.com/): It patches OpenAI's python package and makes it easier to specify and extract complex data structures from OpenAI's API responses.
- [DSPy](https://dspy-docs.vercel.app/): It's a more advanced prompt engineering tool that optimizes the prompt automatically. I think it got a lot of potential, but can be hard to learn.

Although these fancy tools can be very powerful and useful, they sometimes hide the details of the prompts.
I do believe that it's important to read the prompt yourself.
After all, using LLMs is nothing but a conversation.