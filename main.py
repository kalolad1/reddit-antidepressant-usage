import post_analyzer
import post_collector
import post_filterer
import mongodb_helper


def main() -> None:
    collector = post_collector.RedditPostCollector()
    for post in collector.collect_posts():
        if mongodb_helper.post_exists_in_mongodb(post):
            continue

        if post_filterer.filter_post(post):
            post_analyzer.analyze_post(post)
            mongodb_helper.write_post_to_mongodb(post)


if __name__ == "__main__":
    main()
