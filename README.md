# mooddit
Welcome to moodit. This application will parse user and comment thread sentiment from reddit.

The aim of this project is to give users a better understanding of the communities and individuals they are interacting with. Becoming involved in a community that has an overall negative outlook can have and unnoticed effect on a user. Giving better visibility into the overall "vibe" of a community will improve a user's overall online experience.

The website will display rankings of positive / negative communities. If a user is ranked overall positive or negative, it will display the most common pos. / neg. words used, ranked by how impactful they are to the overall ranking.

### Project Goals
1.  Web App Presentation Layer offering a straitforward user exprience.
2.  Optimized importing of user and comment thread text using the Reddit API python library - [praw](https://praw.readthedocs.io/en/stable/).
3.  Track reddit data sentiment utilzing the TextBlob library to calculate text sentiment.
4.  Store API call results in SQL Database for more optimized presentation.
5.  Present to user most positive / negative communities that have been evaluated.



