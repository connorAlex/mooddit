from .tools import get_subreddit, get_user, get_sentiment

#//////////////////////////////////////////////////////////////////////
# Lookup will be the only function called by app.py.
# Other functions are decoupled for debugging and readability purposes.

# See tools.py for functions used.

#//////////////////////////////////////////////////////////////////////

def reddit_lookup(input, type):
    text = []
    # determine what search to conduct
    if type == "subreddit":
        text = get_subreddit(input)
        
    elif type == "user":
        text = get_user(input)

    # get sentiment of data
    return get_sentiment(text)

