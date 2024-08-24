import datetime
from typing import Dict, Generator, List

import praw  # type: ignore[import-not-found]

import drugs
from post import Post

CLIENT_ID = "2PNKUUZ7U8J435ZZF_f19g"
CLIENT_SECRET = "lwnfx-95lv-kQpj39vioHC_Al9_pUw"
USER_AGENT = "test_user_agent"


class RedditPostCollector:

    def __init__(
        self,
        subreddits: List[str] = ["mentalhealth", "depression"],
        subreddit_post_limit: int = 4,
        days: int = 1000,
        keywords: List[str] = drugs.get_antidepressant_search_keywords()[:4],
        client_id: str = CLIENT_ID,
        client_secret: str = CLIENT_SECRET,
        user_agent: str = USER_AGENT,
    ):
        self.reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        self.subreddits = subreddits
        self.subreddit_post_limit = subreddit_post_limit
        self.days = days
        self.keywords = keywords

    def collect_posts(self) -> Generator[Post, None, None]:
        end_time = datetime.datetime.now(datetime.UTC)
        start_time = end_time - datetime.timedelta(days=self.days)

        for subreddit in self.subreddits:
            for keyword in self.keywords:
                for submission in self.reddit.subreddit(subreddit).search(
                    keyword, limit=self.subreddit_post_limit
                ):
                    post_time = datetime.datetime.fromtimestamp(
                        submission.created_utc, datetime.UTC
                    )
                    
                    if start_time <= post_time <= end_time:
                        new_post = Post(
                            title=submission.title,
                            content=submission.selftext,
                            subreddit=subreddit,
                            timestamp=submission.created_utc,
                        )
                        yield new_post
