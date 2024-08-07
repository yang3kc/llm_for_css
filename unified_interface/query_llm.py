"""
This script demonstrates how to query a LLM using a unified interface.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

import api_factory

if __name__ == "__main__":
    # TODO: replace with your own API key
    openai_api_key = "your_openai_api_key"
    google_api_key = "your_google_api_key"
    together_api_key = "your_together_api_key"

    openai_client = api_factory.create_api_client("openai", openai_api_key)
    google_client = api_factory.create_api_client("google", google_api_key)
    together_client = api_factory.create_api_client("together", together_api_key)

    # Define the system prompt and user instruction
    text_message = "The service here is very good!"

    system_prompt = "You are an expert on sentiment analysis. Your job is to evaluate the sentiment of the given text message."
    user_instruction = f"Given the following text message: '{text_message}', please evaluate its sentiment by giving a score in the range of -1 to 1, where -1 means negative and 1 means positive. Also explain why."

    openai_result = openai_client.query_model("gpt-4o", system_prompt, user_instruction)
    print(openai_result)

    google_result = google_client.query_model(
        "gemini-1.5-flash", system_prompt, user_instruction
    )
    print(google_result)

    together_result = together_client.query_model(
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", system_prompt, user_instruction
    )
    print(together_result)
