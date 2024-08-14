import datetime
from typing import Dict, List

import praw  # type: ignore[import-not-found]

import drugs

CLIENT_ID = "2PNKUUZ7U8J435ZZF_f19g"
CLIENT_SECRET = "lwnfx-95lv-kQpj39vioHC_Al9_pUw"
USER_AGENT = "test_user_agent"


class RedditPostCollector:
    def __init__(
        self,
        client_id: str = CLIENT_ID,
        client_secret: str = CLIENT_SECRET,
        user_agent: str = USER_AGENT,
    ):
        self.reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )

    def collect_posts(
        self,
        subreddits: List[str],
        subreddit_post_limit: int,
        days: int,
        keywords: List[str],
    ) -> List[Dict[str, str]]:
        end_time = datetime.datetime.now(datetime.UTC)
        start_time = end_time - datetime.timedelta(days=days)

        collected_posts = []

        for subreddit in subreddits:
            for keyword in keywords:
                for submission in self.reddit.subreddit(subreddit).search(
                    keyword, limit=subreddit_post_limit
                ):
                    post_time = datetime.datetime.fromtimestamp(
                        submission.created_utc, datetime.UTC
                    )
                    if start_time <= post_time <= end_time:
                        collected_posts.append(
                            {"title": submission.title, "selftext": submission.selftext}
                        )
                        # print(collected_posts[-1])

        return collected_posts


if __name__ == "__main__":
    collector = RedditPostCollector()
    SUBREDDITS = ["mentalhealth", "depression"]
    DAYS = 1000
    SUBREDDIT_POST_LIMIT = 2
    KEYWORDS = drugs.get_antidepressant_search_keywords()

    posts = collector.collect_posts(SUBREDDITS, SUBREDDIT_POST_LIMIT, DAYS, KEYWORDS)
