from flask import Flask, request
from bson.json_util import dumps
from data import createUser, createChat, addUserToChat, addMsgToChat, listMsg, analyzeSent, recommender
import os 


app = Flask(__name__)

#createUser
@app.route('/user/create/<name>')
def newUser(name): 
    return createUser(name)


#createChat
@app.route('/chat/create/<name>')
def newChat(name):
    return createChat(name)

#addUserToChat
@app.route('/chat/<chatName>/add/<userName>')
def ChatUserAdd(chatName,userName):
    return addUserToChat(chatName,userName)

#addMessToChat
@app.route('/chat/<chatName>/<userName>/write/<message>')
def ChatMsgAdd(chatName,userName,message):
    return addMsgToChat(chatName,userName,message)


#listMessages
@app.route('/chat/<chatName>/list')
def msgList(chatName):
    return listMsg(chatName)


#analyzeSent
@app.route('/chat/<chatName>/sentiment')
def Sentiments(chatName):
    return analyzeSent(chatName)


#recommender
@app.route('/user/<userName>/recommend')
def recommendation(userName):
    return recommender(userName)

app.run("0.0.0.0", os.getenv("PORT"), debug=True)