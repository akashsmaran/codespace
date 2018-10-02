from flask import request, url_for, Flask
from flask_api import FlaskAPI, status, exceptions
import pyrebase
import numpy as np
import sys
import pandas as pd
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

app = Flask(__name__)

config = {
##    "apiKey": "AIzaSyDaBXErfh1-9lYug3nTKjc1mPYtfFGVEhc",
##    "authDomain": "codespace-29991.firebaseapp.co",
##    "databaseURL": "https://codespace-29991.firebaseio.com",
##    "storageBucket": "codespace-29991.appspot.com",
##    "serviceAccount": "Codespace-d617f5d8e597.json"
    'apiKey': "AIzaSyDaBXErfh1-9lYug3nTKjc1mPYtfFGVEhc",
    'authDomain': "codespace-29991.firebaseapp.com",
    'databaseURL': "https://codespace-29991.firebaseio.com",
    'projectId': "codespace-29991",
    'storageBucket': "",
    'messagingSenderId': "405021268490"
    
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("singhvirohil7@gmail.com", "Rohil@1997") 
user['idToken']
db = firebase.database()


#fatsecret_authentication
consumer_key = 'ee4ecc100aeb44699a44bdc40e59fa42'
consumer_secret = '87be5fa21e414e48b231d505da2dcd0b'

BMR = 0

@app.route("/", methods=['POST'])
def BMR_val():
    weight = request.form['weight']
    height = request.form['height']
    age = request.form['age']
    BMR = 10 * weight + 6.25 * height - 5 * age + 5
    return "You need to be ",BMR," to maintain your weight" 

@app.route("/foodvalue", methods=['POST'])
def foodvalue_update():
    foods = request.form['food_item']
    To_be = BMR
    ans = str(foods[0]['food_description'])
    ans1 = ans.split(" | ")[0]
    ans1 = str(ans1)
    ans2 = ans1.split(": ")[1]
    ans2 = str(ans2)
    ans3 = ans2.split("k")[0]
    ans3 = int(ans3)
    To_be = To_be - ans3
    k = len(db.child().get().val()) - 1
    k = k + 1
    archer = {"Calories":BMR}
    db.child(k).child('me').push(archer,user['idToken'])
    return 'Now you need to consume', To_be,'kCal'

Query = ['hey',
'hi',
'wats up',
'who are you',
'good morning',
'Ssup',
'Whats up',
'Tell me about yourself',
'how are you',
'Where should I eat',
'eating',
'eat',
'I am hungry',
'I want to eat',
'restaurants near me',
'places to eat near me',
'next',
'calories'
]
Intent=[
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Greeting',
'Zomato',
'Zomato',
'Zomato',
'Zomato',
'Zomato',
'Zomato',
'Zomato',
'second',
'second']



    
@app.route('/chatbot', methods=['POST'])
def chatapp():
    chatcontext = request.form['chatcontext']
    #data = pd.read_csv('code.csv')
    #main = data['Query']
    #intent = data['Intent']
    testing = []
    testing.append(chatcontext)
    def text_process(description):
        nopunc = [char for char in description if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [words for words in nopunc.split() if words.lower() not in stopwords.words('english')]

    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
    ])
    pipeline.fit(Query,Intent)
    predictions = pipeline.predict(testing)
    return predictions
    #@app.route("/upload/", methods=['POST'])



if __name__ == "__main__":
    app.run(debug=False)
