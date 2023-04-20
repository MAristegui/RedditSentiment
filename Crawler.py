#!/usr/local/bin/python
import praw
from threading import Thread
import numpy as np
import sqlite3
import StringManipulation as sm
import private
import csv
import threading

# SQLite
cursor = None

# Constants
subredditLimit = 30
hotPostLimit = 300
commentsLimit = None
semPostLimit = 10
semRedditLimit = 10

# Reddit connection
reddit = None

# Reddit connection 
client = private.client
secret = private.secret
agent = private.agent

# Collects data from a comment and its corresponding emotional analysis
# Writes it to a CSV file for later processing
def collectData(textToWrite, emotions):
    wordsCount = len(textToWrite.split(' '))
    emotions = sm.formatEmotions(emotions)

    # Avoid storing data from sentences with few words
    if (wordsCount > 4):
        towrite = [textToWrite]+ [int(num) for num in map(str, emotions)]
        csv_writer.writerow(towrite)


# Thread function that extracts comments and their corresponding emotions from hot posts in a subreddit
# Aggregates the emotions at a subreddit level
def subredditThread(subreddit, result):
    emotionsSubrredit = [0,0,0,0,0,0,0,0,0,0]
    semaphorePost = threading.Semaphore(semPostLimit)

    for post in reddit.subreddit(subreddit.display_name).hot(limit=hotPostLimit):
        semaphorePost.acquire()
        post.comments.replace_more(limit=commentsLimit)
        comment_queue = post.comments[:]  # Seed with top-level

        emotions = [0,0,0,0,0,0,0,0,0,0]
        while comment_queue:
            comment = comment_queue.pop(0)
            cursor=connection.cursor()
            emotionsAux = sm.getEmotions(cursor, comment.body)

            collectData(comment.body,emotionsAux)
            emotions = np.add(emotions,emotionsAux)
            
        emotions = sm.emotionPercentages(emotions)
        emotionsSubrredit = np.add(emotionsSubrredit,emotions)
        semaphorePost.release()

    emotionsSubrredit = sm.emotionPercentages(emotionsSubrredit)

# Returns a Reddit instance to use for accessing the API, creating a new instance if one doesn't already exist,
# Caching it in the global variable 'reddit'            
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

    # Open a CSV file in append mode to store the results of the emotion analysis. Write the column names as the first row.
    csv_file = open('Results.csv', mode='a', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Word', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust'])

       
    reddit = getConnection()
    threads = []
    semaphoreSubreddit = threading.Semaphore(semRedditLimit)

    for subreddit in reddit.subreddits.popular(limit=subredditLimit):
        semaphoreSubreddit.acquire()
        t = Thread(target = subredditThread, args = (subreddit,[] ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
        semaphoreSubreddit.release()
