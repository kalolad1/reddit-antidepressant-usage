import os

import dotenv  # type: ignore[import-not-found]
import pymongo  # type: ignore[import-not-found]

from post import Post

dotenv.load_dotenv()

mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))


def write_post_to_mongodb(post: Post) -> None:
    if post.analysis is None:
        print(f"Post has not been analyzed: {post}")
        return
    
    mongodb_client.online_drug_surveillance_db.posts.insert_one(
        {
            "title": post.title,
            "content": post.content,
            "post_id": post.post_id,
            "analysis": {
                "sentiment": post.analysis.sentiment,
                "adverse_effects": [
                    effect.value for effect in post.analysis.adverse_effects
                ],
                "duration_of_treatment": post.analysis.duration_of_treatment.value,
                "drug": post.analysis.drug,
                "dose": post.analysis.dose,
                "age": post.analysis.age,
                "gender": post.analysis.gender.value,
            },
        }
    )


def post_exists_in_mongodb(post: Post) -> bool:
    return mongodb_client.online_drug_surveillance_db.posts.find_one({"post_id": post.post_id}) is not None
