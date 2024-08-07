import praw
import datetime

class RedditPostCollector:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def collect_posts(self, subreddits, days):
        end_time = datetime.datetime.now(datetime.UTC)
        start_time = end_time - datetime.timedelta(days=days)
        
        collected_posts = []
        
        for subreddit in subreddits:
            for submission in self.reddit.subreddit(subreddit).new(limit=None):
                post_time = datetime.datetime.fromtimestamp(
                    submission.created_utc,
                    datetime.UTC)
                if start_time <= post_time <= end_time:
                    collected_posts.append({
                        'title': submission.title,
                        'author': submission.author.name if submission.author else 'N/A',
                        'score': submission.score,
                        'subreddit': submission.subreddit.display_name,
                        'created_utc': post_time,
                        'url': submission.url,
                        'num_comments': submission.num_comments,
                        'selftext': submission.selftext
                    })
        
        return collected_posts


if __name__ == "__main__":
    client_id = "2PNKUUZ7U8J435ZZF_f19g"
    client_secret = "lwnfx-95lv-kQpj39vioHC_Al9_pUw"
    user_agent = 'test_user_agent'

    collector = RedditPostCollector(client_id, client_secret, user_agent)
    subreddits = ['sebderm']
    days = 1  # Collect posts from the last 7 days

    posts = collector.collect_posts(subreddits, days)
    for post in posts:
        print(post)
