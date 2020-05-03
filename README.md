# API-Project
4th project for Ironhack bootcamp


**_How close are you to your friends? To whichone the most? Is there really good vibes in the chat group?_**

![alt text](INPUT/imagen.jpg)


You can answer those questions that are in the introduction by using the API I have developed in this project. Let me resume you what and how I have worked first; but if you are eager to analyze your chat conversation, you can go directly to "HOW TO USE" head.

### RESUME👨🏻‍💻
The main objective of the project was to develop an API would allow me to send it some parameters and it will respond with an analysis of those variables.

  1.-`/user/create/<username>`
  - **Purpose:** Create a user and save him into DB
  2.- `/user/<user_id>/recommend`
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with top 3 similar users
### 2. Chat endpoints
- (GET) `/chat/create`
  - **Purpose:** Create a conversation to load messages
  - **Params:** An array of users ids `[user_id]`
  - **Returns:** `chat_id`
- (GET) `/chat/<chat_id>/adduser`
  - **Purpose:** Add a user to a chat, this is optional just in case you want to add more users to a chat after it's creation.
  - **Params:** `user_id`
  - **Returns:** `chat_id`
- (POST) `/chat/<chat_id>/addmessage`
  - **Purpose:** Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
  - **Params:**
    - `chat_id`: Chat to store message
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `message_id`
- (GET) `/chat/<chat_id>/list`
  - **Purpose:** Get all messages from `chat_id`
  - **Returns:** json array with all messages from this `chat_id`
- (GET) `/chat/<chat_id>/sentiment`
  - **Purpose:** Analyze messages from `chat_id`. Use `NLTK` sentiment analysis package for this task



### WORK PROCESS 💻 ⚙️

In "Input" folder you will find the initial CSV from which I have worked.
I have clean it, and from it I have developed the main.ipynb file in which I have been looking for the perfect place to locate the office.
The whole code I wrote is in SRC folder.

  - Python 3 
  - Mongodb
  - Modules pandas, numpy and regex. 
  - Request module in order to get some information through some APIs
  - Tableau
  - Visual Studio Code


### WORK DEVELOPMENT 👾🗺











Hope you like it.

LSG
