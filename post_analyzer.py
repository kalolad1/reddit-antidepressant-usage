import csv
import warnings
from typing import Any, Dict, List

import dotenv # type: ignore[import-not-found]
import openai
import pydantic
import transformers # type: ignore[import-not-found]

dotenv.load_dotenv()
client = openai.OpenAI( # type: ignore[attr-defined]
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
        truncation=True)


class PostCharactersticsExtraction(pydantic.BaseModel):
    # adverse_effects: list[str]
    duration_of_treatment: str
    drug: str
    dose: str
    age: int
    gender: str


def get_sentiment_score(post: Dict[str, str]) -> str:
    sentiment = sentiment_analysis_classifier(post["title"] + " " + post["selftext"])
    return str(sentiment[0]["label"])


def get_post_characteristics(post: Dict[str, str]) -> Any:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at structured data extraction. You will be given unstructured text from a reddit post about someones experience with antidepressants and should extract the following characteristics and convert it into the given structure. Use only lowercase. For the drug, provide only a single generic name. If a brand name drug is present convert it to its corresponding generic name.",
            },
            {"role": "user", "content": f"Title: {post["title"]} Body: {post["selftext"]}"},
        ],
        response_format=PostCharactersticsExtraction,
    )

    post_characteristics = completion.choices[0].message.parsed
    return vars(post_characteristics)

def analyze_post(post: Dict[str, str]) -> Any:
    sentiment = get_sentiment_score(post)
    post_characteristics = get_post_characteristics(post)
    return {"sentiment": sentiment} | post_characteristics


def analyze_posts(posts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    analyzed_posts = []
    for post in posts:
        post_analysis = analyze_post(post)
        analyzed_posts.append({"post_id": post["post_id"]} | post_analysis)
        print(analyzed_posts[-1])

    return analyzed_posts


def write_analyzed_posts_to_csv_file(analyzed_posts: List[Dict[str, str]]) -> None:
    # TODO: Ensure that individual fields do not contain commas, or if they do, quote them
    with open("analyzed_posts.csv", "w") as file:
        file.write("post_id,sentiment,duration_of_treatment,drug,dose,age\n")
        for post in analyzed_posts:
            post_id = post["post_id"]
            sentiment = post["sentiment"]
            # adverse_effects = post["adverse_effects"]
            duration_of_treatment = post["duration_of_treatment"]
            drug = post["drug"]
            dose = post["dose"]
            age = post["age"]

            file.write(f"{post_id},{sentiment},{duration_of_treatment},{drug},{dose},{age}\n")



def read_posts_from_csv_file(file_path: str) -> List[Dict[str, str]]:
    posts = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            posts.append({"title": row["title"], "selftext": row["selftext"], "post_id": row["post_id"]})
    return posts


if __name__ == "__main__":
    posts = read_posts_from_csv_file("filtered_posts.csv")
    print(f"Total posts to analyze: {len(posts)}")

    analyzed_posts = analyze_posts(posts)
    write_analyzed_posts_to_csv_file(analyzed_posts)
