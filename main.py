import logging

import post_analyzer
import post_collector
import post_filterer
import mongodb_helper

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main logger")
logger.setLevel(logging.INFO)


def main() -> None:
    collector = post_collector.RedditPostCollector()
    analyzed_posts = 0
    for post in collector.collect_posts():
        logger.info(f"Collecting Post: {post.title.rstrip()}")

        if mongodb_helper.post_exists_in_mongodb(post):
            logger.info(
                f"Post: {post.title.rstrip()} already exists in MongoDB. Skipping.\n"
            )
            continue

        if post_filterer.filter_post(post):
            post_analyzer.analyze_post(post)
            logger.info(f"Post: {post.title.rstrip()} analyzed.")

            mongodb_helper.write_post_to_mongodb(post)
            logger.info(
                f'{analyzed_posts}: "{post.title.rstrip()}" written to MongoDB.'
            )
            logger.info(f"Total posts analyzed so far: {analyzed_posts}\n")
            analyzed_posts += 1


if __name__ == "__main__":
    main()
