import csv
import enum
import warnings
from typing import Any, Dict, List

import dotenv  # type: ignore[import-not-found]
import openai
import pydantic
import transformers  # type: ignore[import-not-found]

from post import Post, AdverseEffect, DurationOfTreatment, Gender
from mongodb_helper import mongodb_client

dotenv.load_dotenv()
client = openai.OpenAI(  # type: ignore[attr-defined]
    api_key="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",
)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_analysis_classifier = transformers.pipeline(
        "text-classification",
        model=model_path,
        tokenizer=model_path,
        max_length=512,
        truncation=True,
    )


class PostCharactersticsExtraction(pydantic.BaseModel):
    adverse_effects: list[AdverseEffect]
    duration_of_treatment: DurationOfTreatment
    drug: str
    dose: str
    age: int
    gender: Gender


def get_sentiment_score(post: Post) -> str:
    sentiment = sentiment_analysis_classifier(post.title + " " + post.content)
    return str(sentiment[0]["label"])


POST_CHARACTERSTICS_PROMPT = """
You are an expert at structured data extraction. 

You will be given unstructured text from a reddit post about 
someones experience with antidepressants and should extract 
the following characteristics and convert it into the given structure.

For the drug, provide only a single generic name.
If a brand name drug is present convert it to its corresponding generic name.

If the post does not contain a specific characteristic, leave it blank.

If the post contains multiple values for a characteristic,
choose the most relevant one.

Lowercase all text.
"""


def get_post_characteristics(post: Post) -> Any:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": POST_CHARACTERSTICS_PROMPT,
            },
            {"role": "user", "content": f"Title: {post.title} Body: {post.content}"},
        ],
        response_format=PostCharactersticsExtraction,
    )

    extraction = completion.choices[0].message
    return vars(extraction.parsed)


def analyze_post(post: Post) -> None:
    sentiment = get_sentiment_score(post)
    post_characteristics = get_post_characteristics(post)

    post.age = post_characteristics["age"]
    post.gender = post_characteristics["gender"]
    post.drug = post_characteristics["drug"]
    post.dose = post_characteristics["dose"]
    post.duration_of_treatment = post_characteristics["duration_of_treatment"]
    post.adverse_effects = post_characteristics["adverse_effects"]
    post.sentiment = sentiment


def read_posts_from_mongodb() -> List[Post]:
    posts = []
    for post in mongodb_client.online_drug_surveillance_db.filtered_posts.find():
        new_post = Post(
            title=post["title"],
            content=post["content"],
        )
        posts.append(new_post)
    return posts
