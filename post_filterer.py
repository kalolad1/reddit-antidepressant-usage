import csv
import json
import os
from typing import Dict, List

import openai

import drugs
import post_collector
from mongodb import mongodb_client
from post import Post

# Set up OpenAI API key
client = openai.OpenAI(  # type: ignore[attr-defined]
    api_key="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",
)


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
        print(post.title)
        print(post.content)
        print(result)
        print("\n\n\n")
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


def main() -> None:
    collector = post_collector.RedditPostCollector()
    SUBREDDITS = ["mentalhealth", "depression"]
    DAYS = 1000
    SUBREDDIT_POST_LIMIT = 2
    KEYWORDS = drugs.get_antidepressant_search_keywords()

    # TODO: Remove this line, only for testing
    KEYWORDS = KEYWORDS[:2]

    posts = collector.collect_posts(SUBREDDITS, SUBREDDIT_POST_LIMIT, DAYS, KEYWORDS)
    print(f"Total posts collected: {len(posts)}")

    filtered_posts = filter_posts(posts)
    print(f"Total posts filtered: {len(filtered_posts)}")

    write_posts_to_mongodb(filtered_posts)
    write_posts_to_csv_file(filtered_posts)


if __name__ == "__main__":
    main()
