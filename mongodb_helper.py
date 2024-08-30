import os

import dotenv
import pymongo  # type: ignore[import-not-found]

from post import Post

dotenv.load_dotenv()

mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))


def write_post_to_mongodb(post: Post) -> None:

    mongodb_client.online_drug_surveillance_db.posts.insert_one(
        {
            "title": post.title,
            "content": post.content,
            "subreddit": post.subreddit,
            "timestamp": post.timestamp,
            "post_id": post.post_id,
            "age": post.age,
            "gender": post.gender.value if post.gender is not None else "",
            "drug": post.drug,
            "dose": post.dose,
            "duration_of_treatment": (
                post.duration_of_treatment.value
                if post.duration_of_treatment is not None
                else ""
            ),
            "adverse_effects": [effect.value for effect in post.adverse_effects],
            "sentiment": post.sentiment,
        }
    )


def post_exists_in_mongodb(post: Post) -> bool:
    return (
        mongodb_client.online_drug_surveillance_db.posts.find_one(
            {"post_id": post.post_id}
        )
        is not None
    )
