DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS subreddit;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    pos FLOAT,
    neg FLOAT,
    neu FLOAT,
    compound FLOAT,
    date_added TEXT
);

CREATE TABLE subreddit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pos FLOAT,
    neg FLOAT,
    neu FLOAT,
    compound FLOAT,
    date_added TEXT
);