import random

from mongodb_helper import mongodb_client


def select_human_validation_set() -> None:
    # Connect to MongoDB
    db = mongodb_client.online_drug_surveillance_db
    posts_collection = db.posts
    validation_collection = db.human_validation_set

    # Retrieve all post IDs
    post_ids = posts_collection.distinct("post_id")

    # Select 100 random post IDs
    selected_post_ids = random.sample(post_ids, 100)

    # Retrieve the selected posts
    selected_posts = posts_collection.find(
        {"post_id": {"$in": selected_post_ids}},
        {"title": 1, "content": 1, "post_id": 1},
    )

    # Insert the selected posts into the human_validation_set collection
    validation_collection.insert_many(selected_posts)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
