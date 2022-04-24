DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS subreddit;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pos FLOAT,
    neg FLOAT,
    NEU FLOAT,
    compound FLOAT,
    date_added DATETIME
);

CREATE TABLE subreddit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sub_name TEXT NOT NULL,
    pos FLOAT,
    neg FLOAT,
    neu FLOAT,
    compound FLOAT,
    date_added DATETIME
);