#!/usr/local/bin/python
import praw
from threading import Thread
import numpy as np
import sqlite3

import StringManipulation as sm
import private

# Cleaning spyder console 
print("\014")
cursor = None

# Constants
subredditLimit = 1
hotPostLimit = 3
commentsLimit = 10
reddit = None

# Reddit connection 
client = private.client
secret = private.secret
agent = private.agent

def subredditThread(subreddit, result):
    emotionsSubrredit = [0,0,0,0,0,0,0,0,0,0]
    for post in reddit.subreddit(subreddit.display_name).hot(limit=hotPostLimit):
        post.comments.replace_more(limit=commentsLimit)
        comment_queue = post.comments[:]  # Seed with top-level
        emotions = [0,0,0,0,0,0,0,0,0,0]
        
        while comment_queue:
            comment = comment_queue.pop(0)
            emotions = np.add(emotions,sm.getEmotions(cursor, comment.body))
            
        emotions = sm.emotionPercentages(emotions)
        emotionsSubrredit = np.add(emotionsSubrredit,emotions)
    emotionsSubrredit = sm.emotionPercentages(emotionsSubrredit)
            
def getConnection():
    global reddit
    if (reddit == None):
        reddit = praw.Reddit(client_id=client, 
                             client_secret=secret, 
                             user_agent=agent,
                             check_for_async=False)
    return reddit

if __name__ == "__main__":
    
    # Connection to database
    connection=sqlite3.connect('db_Emotions.db',check_same_thread=False)
    cursor=connection.cursor()
       
    reddit = getConnection()
    threads = []
    for subreddit in reddit.subreddits.popular(limit=subredditLimit):
        t = Thread(target = subredditThread, args = (subreddit,[] ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()