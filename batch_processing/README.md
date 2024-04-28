# Introduction

This folders contains instructions and example code for using [OpenAI's batch API](https://platform.openai.com/docs/api-reference/batch) to process large amounts of data with reduced cost.
The idea is simple, you put all your prompts in a file, upload the file to OpenAI's server, and wait for up to 24 hours the responses (my tests show that it's much faster than that actually, but this might change).

Here, I'm going to use the same sentiment analysis example for demonstration.
Since the operation requires a lot of interactive commands, I'll use a Jupyter notebook this time.
You can check it out [here](/batch_processing/batch_processing.ipynb).

Note that OpenAI's website provides UI to control the batch processing.
So you could use a script to generate the batch file (the prompts), and then use the website UI to upload the file, create batch job, check the status, and download the results.
Here is a [script](/batch_processing/create_batch_file.py) to help you create the batch file.

Finally, OpenAI has a nice [demonstration](https://github.com/openai/openai-cookbook/blob/main/examples/batch_processing.ipynb) on using the batch API, and you should check it out.