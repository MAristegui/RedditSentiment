import csv
import sqlite3

# Cleaning spyder console 
print("\014")


with open('nrc_emotion_lexicon.csv' , 'r') as csvfile:
    
    csv_file_reader = csv.reader(csvfile,delimiter=',')
    # Skip the first row
    next(csv_file_reader,None)
    
    # Create fields
    Word = ''
    Positive = ''
    Negative = ''
    Anger = ''
    Anticipation = ''
    Disgust = ''
    Fear = ''
    Joy = ''
    Sadness = ''
    Surprise = ''
    Trust = ''
    
    # Create the query   
    Table_Query = '''CREATE TABLE if not Exists EmotionLexicon 
    (Word TEXT UNIQUE,
     Positive INT,
     Negative INT,
     Anger INT,
     Anticipation INT,
     Disgust INT,
     Fear INT,
     Joy INT,
     Sadness INT,
     Surprise INT,
     Trust INT)'''
    
    # Create database and table
    connection=sqlite3.connect('db_Emotions.db')
    cursor=connection.cursor()
    #cursor.execute('DELETE FROM EmotionLexicon;',);
    cursor.execute(Table_Query)
    
    # Complete the query
    for row in csv_file_reader:
        # skip the first row
        for i in range(len(row)):
            # assign each field its value
            row = row[0].split(';')
            Word = row[0]
            Positive = row[1]
            Negative = row[2]
            Anger = row[3]
            Anticipation = row[4]
            Disgust = row[5]
            Fear = row[6]
            Joy = row[7]
            Sadness = row[8]
            Surprise = row[9]
            Trust = row[10]
        
        cursor.execute('''CREATE TABLE EmotionLexicon (Word TEXT NOT NULL, Positive INT, Negative INT,Anger INT, Anticipation INT,Disgust INT,Fear INT,Joy INT,Sadness INT,Surprise INT,Trust INT);''')
        # Insert rows into the database
        InsertQuery=f"INSERT INTO EmotionLexicon VALUES ('{Word}','{Positive}','{Negative}','{Anger}','{Anticipation}','{Disgust}','{Fear}','{Joy}','{Sadness}', '{Surprise}','{Trust}')"
        cursor.execute(InsertQuery)
    
    
    connection.commit()
    connection.close()
    