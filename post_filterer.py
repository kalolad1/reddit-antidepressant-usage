import csv
import json
import os
from typing import Dict, List

import openai

import drugs
import post_collector
from mongodb_helper import mongodb_client
from post import Post

# Set up OpenAI API key
client = openai.OpenAI(  # type: ignore[attr-defined]
    api_key="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",
)


def filter_post(post: Post) -> bool:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Does this Reddit post discuss a person's individual experience taking an antidepressant drug? Title: {post.title}  Body: {post.content} Response with only the words 'yes' or 'no' if this post describes the person's experience taking the drug. Do not include punctuation.",
            },
        ],
    )
    result = completion.choices[0].message.content.strip().lower()
    return "yes" in result


def filter_posts(posts: List[Post]) -> List[Post]:
    filtered_posts = []
    for post in posts:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Does this Reddit post discuss a person's individual experience taking an antidepressant drug? Title: {post.title}  Body: {post.content} Response with only the words 'yes' or 'no' if this post describes the person's experience taking the drug. Do not include punctuation.",
                },
            ],
        )
        result = completion.choices[0].message.content.strip().lower()
        if "yes" in result:
            filtered_posts.append(post)
    return filtered_posts


def write_posts_to_csv_file(posts: List[Post]) -> None:
    with open("filtered_posts.csv", "w", newline="") as file:
        fieldnames = ["title", "content", "post_id"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for post in posts:
            writer.writerow(
                {
                    "title": post.title,
                    "content": post.content,
                    "post_id": post.post_id,
                }
            )


def write_posts_to_mongodb(posts: List[Post]) -> None:
    mongodb_client.online_drug_surveillance_db.filtered_posts.insert_many(
        [
            {
                "title": post.title,
                "content": post.content,
                "post_id": post.post_id,
            }
            for post in posts
        ]
    )
