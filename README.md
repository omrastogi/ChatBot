# Ajax-ChatBot

Chatbot has five parts - 

1. Model - simple bag-of-word with a Sequencial Network

Build - Input -> 128 Dense[Relu] -> Dropout of 0.5 -> 64 Dense [Relu] -> Dropout of 0.5 -> Softmax -> Output 

2. SQL - To save the messages but the bot and user

3. Backend - A flask backend to communicate with javascript via AJAX and updates the SQL
 
 SQL <-----> Flask <--AJAX--> JS <--- SQL  

4. Frontend - The frontend is HTML,CSS and Bootstrap

5. Dataset - Intent.json is given question and answer with tags
