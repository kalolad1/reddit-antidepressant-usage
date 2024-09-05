import logging

from post import Post
import post_analyzer
import post_collector
import post_filterer
import mongodb_helper

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main logger")
logger.setLevel(logging.INFO)


def process_post(post: Post) -> bool:
    # Filters, analyzes, and writes a post to MongoDB
    logger.info(f"Collecting Post: {post.title.rstrip()}")
    if mongodb_helper.post_exists_in_mongodb(post):
        logger.info(f"Post already exists in MongoDB. Skipping.\n")
        return False

    if post_filterer.filter_post(post):
        post_analyzer.analyze_post(post)
        logger.info(f"Post analyzed.")

        mongodb_helper.write_post_to_mongodb(post)
        logger.info(f"Post written to MongoDB.")

    return True


def main() -> None:
    SUBREDDIT_POST_LIMIT = 1000000
    
    # 10 years
    DAYS = 3650
    collector = post_collector.RedditPostCollector(
        subreddit_post_limit=SUBREDDIT_POST_LIMIT, days=DAYS
    )

    # Skip the first N posts because they might have already been read
    num_posts_skip_ahead = 0
    analyzed_posts = 0
    for post in collector.collect_posts():
        if num_posts_skip_ahead > 0:
            num_posts_skip_ahead -= 1
            continue
        try:
            if process_post(post):
                analyzed_posts += 1
                logger.info(f"Total posts analyzed so far: {analyzed_posts}\n")
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
