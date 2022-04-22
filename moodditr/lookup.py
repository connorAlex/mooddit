from urllib.parse import uses_fragment
import praw

reddit = praw.Reddit("mooddit", user_agent = "mooddit user agent")
reddit.read_only = True
for submission in reddit.subreddit("learnpython").hot(limit=10):
    print(submission.title)