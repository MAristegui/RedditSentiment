import numpy as np
import sqlite3
import re
import nltk
from nltk.corpus import stopwords
import string
nltk.download('stopwords')

# Constants
maxDecimals = 2

stemmer = nltk.SnowballStemmer("english")
stopword=set(stopwords.words('english'))

# Remove non-alphabetic characters from a text
def cleanString(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    return text

# Format emotions (for data collection)   
def formatEmotions(emotions):
    return [1 if i != 0 else 0 for i in emotions]

# Pending implementation
def wordsLearning():
    # Pending
     return 0
 
# Calculate percentages of emotions
def emotionPercentages(emotions):
    total = sum(emotions)
    toRet = [0,0,0,0,0,0,0,0,0,0]
    
    if (total != 0):
        for x in range(len(emotions)):
            toRet[x] = (emotions[x]*100)/total
        toRet = np.round(toRet,maxDecimals)
    
    return toRet

#Get the emotions associated with a comment    
def getEmotions(cursor, comment):
    words = cleanString(comment)
    emotions = [0,0,0,0,0,0,0,0,0,0]
    newWords = []
    
    for word in words:      
        cursor.execute("SELECT * FROM EmotionLexicon WHERE WORD=?", (word,))
        rows = cursor.fetchall()
        
        if (len(rows) == 0):
            newWords.append(word)
        else:
            for row in rows:
                emotions = np.add(emotions,row[1:])
                  
    return emotions
    