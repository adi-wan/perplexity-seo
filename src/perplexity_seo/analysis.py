#!/usr/bin/env python3

import sys
from typing import Literal
sys.path.append("./.packages")

from pydantic import BaseModel
from openai import OpenAI
from perplexity_seo.providers.perplexity import Perplexity

class Sentiment(BaseModel):
    sentiment: Literal["thumbsup", "thumbsdown"]


client = OpenAI()

schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentiment",
        "schema": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "description": "A representation of a blog post",
            "type": "object",
            "required": ["sentiment"],
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["thumbsup", "thumbsdown"]
                }
            },
            "strict": True
        }
    }
}



def compare_response_against_expectation(response: str, expectation: str) -> Literal["thumbsup", "thumbsdown"]:
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        response_format=schema,
        messages=[
            {"role": "developer", "content": expectation},
            {"role": "user", "content": response},
        ]
    )
    return Sentiment.model_validate_json(completion.choices[0].message.content).sentiment


if __name__ == "__main__":
    expectation = input("Enter your expectation: ")
    prompt = input("Enter your search query: ")
    
    perplexity = Perplexity()
    response = perplexity.query(prompt)
    
    result = compare_response_against_expectation(response, expectation)
    print(f"Result: {result}")
