"""
This file defines a set of classes to support different providers and a function `create_api_client` to create a client for a given provider.

Author: Kaicheng Yang <yang3kc@gmail.com>
"""

from together import Together
import google.generativeai as genai
from openai import OpenAI


class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = self._create_api_client()

    def _create_api_client(self):
        raise NotImplementedError

    def query_model(self, model, system_prompt, user_instruction):
        raise NotImplementedError


class OpenAIClient(APIClient):
    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_api_client(self):
        return OpenAI(api_key=self.api_key)

    def query_model(self, model, system_prompt, user_instruction):
        completion = self.client.chat.completions.create(
            model=model,
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_instruction},
            ],
        )
        return completion.choices[0].message.content


class TogetherClient(APIClient):
    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_api_client(self):
        return Together(api_key=self.api_key)

    def query_model(self, model, system_prompt, user_instruction):
        prompt = system_prompt + user_instruction
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"content": prompt, "role": "user"}],
            max_tokens=2046,
            temperature=0,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>"],
            stream=False,
        )
        return response.choices[0].message.content


class GoogleClient(APIClient):
    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_api_client(self):
        genai.configure(api_key=self.api_key)
        return genai

    def query_model(self, model, system_prompt, user_instruction):
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        model = self.client.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            safety_settings="BLOCK_NONE",
            system_instruction=system_prompt,
        )
        resp = model.generate_content(user_instruction)
        return resp.text


def create_api_client(provider, api_key):
    provider_mapping = {
        "openai": OpenAIClient,
        "together": TogetherClient,
        "google": GoogleClient,
    }
    if provider not in provider_mapping:
        raise ValueError(
            f"Unknown provider: {provider}, must be one of {provider_mapping.keys()}"
        )
    return provider_mapping[provider](api_key)
