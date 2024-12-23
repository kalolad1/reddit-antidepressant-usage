import os

import dotenv
import pymongo  # type: ignore[import-not-found]

from post import Post

dotenv.load_dotenv()

mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))


def write_post_to_mongodb(post: Post) -> None:
    mongodb_client.online_drug_surveillance_db.posts_v2.insert_one(
        {
            "title": post.title,
            "content": post.content,
            "subreddit": post.subreddit,
            "timestamp": post.timestamp,
            "post_id": post.post_id,
            "age": post.age,
            "gender": post.gender.value if post.gender is not None else "",
            "drugs_used": [
                {
                    "name": drug.name,
                    "adverse_effects": [
                        adverse_effect.value for adverse_effect in drug.adverse_effects
                    ],
                    "duration_of_treatment": drug.duration_of_treatment.value,
                    "dose": drug.dose,
                }
                for drug in post.drugs_used
            ],
            "sentiment": post.sentiment,
        }
    )


def post_exists_in_mongodb(post: Post) -> bool:
    return (
        mongodb_client.online_drug_surveillance_db.posts_v2.find_one(
            {"post_id": post.post_id}
        )
        is not None
    )


def update_post_in_mongodb(post_id: str, update: dict) -> None:
    result = mongodb_client.online_drug_surveillance_db.posts_v2.update_one(
        {"post_id": post_id}, update
    )

    if result.modified_count == 0:
        print(f"Post with ID {post_id} not changed.")
    else:
        print(f"Post with ID {post_id} updated in MongoDB.")


def get_all_posts():
    return mongodb_client.online_drug_surveillance_db.posts_v2.find()
