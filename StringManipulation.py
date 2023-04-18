import numpy as np
import sqlite3
import re
import nltk
from nltk.corpus import stopwords
import string
nltk.download('stopwords')

# Cleaning spyder console 
print("\014")

# Constants
maxCharacters = 3
maxDecimals = 2

stemmer = nltk.SnowballStemmer("english")
stopword=set(stopwords.words('english'))

# Removing all non-alpha characters from a text
def cleanString(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    return text


def wordsLearning():
    # Pending
     return 0
    

def emotionPercentages(emotions):
    
    total = sum(emotions)
    toret = [0,0,0,0,0,0,0,0,0,0]
    
    if (total != 0):
        for x in range(len(emotions)):
            toret[x] = (emotions[x]*100)/total
        toret = np.round(toret,2)
    
    return toret
    
def getEmotions(cursor, comment):
    
    words = cleanString(comment.lower())
    
    emotions = [0,0,0,0,0,0,0,0,0,0]
    newWords = []
    
    for word in words:
        res = cursor.execute("SELECT * FROM EmotionLexicon WHERE WORD=?", (word,))
        rows = res.fetchall()
        
        if (len(rows) == 0):
            newWords.append(word)
        else:
            for row in rows:
                emotions = np.add(emotions,row[1::])
                  
    return emotions
    
