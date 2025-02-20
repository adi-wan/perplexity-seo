#!/usr/bin/env python3

import os
import sys
sys.path.append("./.packages")

from pydantic import BaseModel

class Sentiment(BaseModel):
    sentiment: str

from openai import OpenAI
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
                    "type": "string"
                }
            },
            "strict": True
        }
    }
}

expectation = """
Compare the given content with following expectation and give the sentiment back.

Available sentiment options are: thumbsup or thumbsdown

At least contains following banks

- J.P. Morgan Chase
- Bank of America
- Citibank
- Wells Fargo
- U.S. Bank
- PNC Bank
- Goldman Sachs Bank
- Truist Bank
- Sparkasse

The total assets should be also mentioned for each bank on the list

Compare the given content with the expected bank list above and and give the sentiment back.

Available sentiment options are: thumbsup or thumbsdown

Only return one word: thumbsup or thumbsdown
"""

perplexity = """
The top 10 banks in the United States, ranked by total assets as of mid-2024, are as follows:

| Rank | Bank                | Total Assets (in trillions) |
|------|---------------------|-----------------------------|
| 1    | Chase Bank          | $3.51                       |
| 2    | Bank of America     | $2.55                       |
| 3    | Wells Fargo         | $1.72                       |
| 4    | Citibank            | $1.69                       |
| 5    | U.S. Bank           | $0.6649                     |
| 6    | PNC Bank            | $0.5525                     |
| 7    | Goldman Sachs Bank   | $0.5439                     |
| 8    | Truist Bank         | $0.5119                     |
| 9    | Capital One         | $0.4773                     |
| 10   | TD Bank             | $0.3703                     |

These banks collectively manage approximately **$12.56 trillion** in assets, making them the largest financial institutions in the country[1][2][3].

Citations:
[1] https://www.experian.com/blogs/ask-experian/largest-banks-in-us/
[2] https://www.mx.com/blog/biggest-banks-by-asset-size-united-states/
[3] https://en.wikipedia.org/wiki/List_of_largest_banks_in_the_United_States
[4] https://www.federalreserve.gov/releases/lbr/current/
[5] https://www.usnews.com/banking/articles/biggest-banks-in-america
[6] https://www.businessinsider.com/personal-finance/banking/best-banks
[7] https://www.forbes.com/lists/americas-best-banks/
"""

print(expectation)

completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    response_format=schema,
    messages=[
        {"role": "developer", "content": expectation},
        {"role": "user", "content": "write a haiku about ai"},
    ]
)

print(completion.choices)

completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    response_format=schema,
    messages=[
        {"role": "developer", "content": expectation},
        {"role": "user", "content": perplexity},
    ]
)

print(completion.choices)