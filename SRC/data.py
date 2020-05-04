import pymongo
import random
import requests
from error_handler import jsonErrorHandler
from configuration import DBURL
from bson.json_util import dumps
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np

#BBDD

client=pymongo.MongoClient(DBURL)
print(f"Connected to {DBURL}")


mydb = client.get_default_database()
userColl = mydb['users']
chatColl = mydb['chats']


#Create a new user

@jsonErrorHandler
def createUser(name):
    dic = {
            "_id": max(userColl.distinct('_id'))+1,
            "name": name }
    if not userColl.find_one({'name':name}):
        x = userColl.insert_one(dic)
        return f'User {name} created with id number: {x.inserted_id}'
    else:
        return 'User already exists'



#Create a new chat 

@jsonErrorHandler
def createChat(name):
    dic = {
            "_id": max(chatColl.distinct('_id'))+1,
            "name": name,
            "users": [],
            "messages":[]
            }
    if not chatColl.find_one({'name':name}):
        x = chatColl.insert_one(dic)
        return f'Chat {name} created with id number: {x.inserted_id}'
    else:
        return 'Chat already exists'



#Add users to an existing chat

@jsonErrorHandler
def addUserToChat(chatName,userName):
    if not chatColl.find_one({'name':chatName}): 
        if not userColl.find_one({'name':userName}):
            return 'Neither chat and user exist, you must create them both. Use this route /user/create/name for creating an user and this /chat/create/name for an user.'
        else:
            return 'Chat does not exist. You must create it using this route /chat/create/name'
    else:
        if not userColl.find_one({'name':userName}):
            return 'User {userName} does not exist. You must create it using this route /user/create/name'
        else:
            if not chatColl.find_one({'users.name':userName}):
                chatColl.update({ "name": chatName },{ "$push": { "users": userColl.find_one({'name':userName}) } })
                return f'User {userName} added to chat: {chatName}'
            else:
                return f'User {userName} was already in chat: {chatName}'



#Add messages to an existing chat (send by an existing user in an existing chat)

@jsonErrorHandler
def addMsgToChat(chatName,userName, message):
    if not chatColl.find_one({'name':chatName}): 
        return 'Chat does not exist. You must create it using this route /chat/create/name'
    else:
        if not userColl.find_one({'name':userName}):
            return f'User {userName} does not exist. You must create it using this route /user/create/name'
        else:
            if not chatColl.find_one({'users.name':userName}):
                return f'User {userName} is not in chat: {chatName}. You must add it using this route /chat/chatName/add/userName'
            else:
               chatColl.update({"name": chatName},{"$push":{"messages":{"user": userName,"message":message}}})
               return f'Message sent successfully'
           


#Show all messages of an existing chat

@jsonErrorHandler
def listMsg(chatName):
    if not chatColl.find({"name":chatName}):
        return 'Chat does not exist. You must create it using this route /chat/create/name'
    else: 
        res = chatColl.find({"name":chatName},{"_id":0,"messages":1})
        return res[0]


#Analyze messages´ sentiments from a chat

@jsonErrorHandler
def analyzeSent(chatName):
    if not chatColl.find({"name":chatName}):
        return 'Chat does not exist. You must create it using this route /chat/create/name'
    else: 
        all_text = chatColl.find({"name":chatName},{"_id":0,"messages":1})
        text=all_text[0]
        filter_text = ' '.join(e["message"] for e in text["messages"])
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(filter_text)



#Recommends other users for a given user

@jsonErrorHandler
def recommender(userName):
    #I generate a df with all messages and users
    count_vectorizer = CountVectorizer()
    allMesgs = chatColl.find({},{"_id":0,"messages":1})
    usr = []
    msg = []
    for e in allMesgs:
        for i in e['messages']:
            usr.append(i['user'])
            msg.append(i['message'])
    df = pd.DataFrame({"Users":usr,"Messages":msg})
    df = pd.DataFrame(df.groupby("Users")["Messages"].apply(list))
    df['Messages'] = df['Messages'].apply(lambda texto: " ".join(texto))
    df=df.reset_index()
    data = { e:i for e,i in zip(list(df['Users']),list(df['Messages']))}
    #Generate a matrix in order to normalize data info
    sparse_matrix = count_vectorizer.fit_transform(data.values())
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                    columns=count_vectorizer.get_feature_names(),
                    index=data.keys())
    #Proximity matrix 
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(
        similarity_matrix, columns=data.keys(), index=data.keys())
    #Droping diagonal values because its a comparation with themselves
    np.fill_diagonal(sim_df.values, 0)
    #Getting the most similar character
    similarities_to ={ sim_df.idxmax().loc[userName] : sim_df[userName].max() }
    return similarities_to
   
   
    