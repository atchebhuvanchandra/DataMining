'''
Created on 29-Apr-2018

@author: Hari
'''


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.twitter
collection = db.tweets
for tweet in collection.find():
    print(tweet["text"].encode('utf-8'))
    