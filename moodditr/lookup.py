import praw
from praw.models import MoreComments
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit("mooddit", user_agent = "mooddit user agent")
reddit.read_only = True
analyzer = SentimentIntensityAnalyzer()


def reddit_lookup(input, type):
    text = []
    # determine what search to conduct
    if type == "/r/":
        text = get_subreddit(input)
        
    elif type == "/u/":
        text = get_user(input)

    # get sentiment of data
    return get_sentiment(text)


def get_user(user):
    comments = []

    # Get user using redditor() method
    redditor = reddit.redditor(user)

    # Get all comments user has posted

    for item in redditor.comments.new(limit=None):
        comments.append(item.body)
    
    return comments

def get_subreddit(sub):
    
    top_comments = []

    # Get subreddit from param
    subreddit = reddit.subreddit(sub)
    
    # Loop through submissions, 25 posts in the front page
    for submission in subreddit.top("month", limit=25):

        # Loop through all the comments in the submission
        for item in submission.comments.list():
            
            if isinstance(item, MoreComments):
                continue

            # Append the comment to the top_comments list
            top_comments.append(item.body)

    return top_comments

def get_sentiment(text):
    score = {
        'pos':0,
        'neu':0,
        'neg':0,
        'compound':0
    }

    num_comments = len(text)
    
    
    # Loop through text, get polarity score
    for item in text:
        # get the vader score for the specific comment
        vs = analyzer.polarity_scores(item)

        # Check to see that vader actually performed an anlysis on the phrase
        if vs['pos'] != 0 and vs['compound'] != 0 and vs['neu'] != 0 and vs['neg'] != 0:
            score['compound'] += (vs['compound'])
            score['pos'] += (vs['pos'])
            score['neu'] += (vs['neu'])
            score['neg'] += (vs['neg'])
            
        else:
            # if it didn't add the score, we need to drop the average denom. by 1
            num_comments -= 1
    
    # Avg the sentiment score
    score['compound'] /= num_comments
    score['pos'] /= num_comments
    score['neu'] /= num_comments
    score['neg'] /= num_comments

    return score

