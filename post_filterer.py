import json
import os

import openai

import drugs
import post_collector

# Set up OpenAI API key
client = openai.OpenAI(
    api_key="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",
)

def filter_posts(posts):
    filtered_posts = []
    for post in posts:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Does this Reddit post discuss a person's individual experience taking an antidepressant drug? Title: {post['title']}  Body: {post['selftext']} Response with only the words 'yes' or 'no' if this post describes the person's experience taking the drug. Do not include punctuation.",
                },
            ],
        )
        result = completion.choices[0].message.content.strip().lower()
        # print(post['selftext'])
        # print(result)
        # print('\n\n\n')
        if "yes" in result:
            filtered_posts.append(post)
    return filtered_posts

def write_posts_to_csv_file(posts):
    with open("filtered_posts.csv", "w") as file:
        file.write("title,selftext\n")
        for post in posts:
            file.write(f"{post['title']},{post['selftext']}\n")

def main():
    collector = post_collector.RedditPostCollector()
    SUBREDDITS = ["mentalhealth", "depression"]
    DAYS = 1000
    SUBREDDIT_POST_LIMIT = 2
    KEYWORDS = drugs.get_antidepressant_search_keywords()

    posts = collector.collect_posts(SUBREDDITS, SUBREDDIT_POST_LIMIT, DAYS, KEYWORDS)

    # Filter posts
    filtered_posts = filter_posts(posts)

    write_posts_to_csv_file(filtered_posts)


if __name__ == "__main__":
    main()
