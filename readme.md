The Project Consist of multiple branches - 
1. Bag Of Word Approch 
2. Bert Question and Answering Approch 
3. Attention Based model
4. Semantic Search 
5. Ajax based chatbot deployment



An End-To-End Integrable Intelligent Chatbot 

Abstract 
This project aims to create a solution to provide an intelligent querying system that responds like a human i.e. Conversation AI. This article provides multiple intelligent systems and deployment options to make it integrable with websites. This work explores simpler methods like a bag-of-word model and word-embedding-based models than other methods using pre-trained models like Bert/Roberta i.e. semantic search and Question-Answering. 

Introduction 
In businesses specially B2Cs, a lot of resources and efforts have to be put into reaching potential customers and solving their queries. A huge amount of resources and time goes into just calling and messaging potential clients, yet the efficiency and effectiveness are very difficult to achieve especially for small businesses. 

The objective is to create a querying system that can minimize human intervention by providing conversation-like responses to questions and doubts. The chatbot is aimed to be easily integrable with few lines of code. 

The ai problem has two parts - 
Intelligent Querying: For understanding the context of the question and getting the answer 
Conversation AI: Understanding the language flow of questions to embed the answers into conversational statements 

The integration has the following domain - 
API: To integrate the ai system with an API and create API calls from the frontend
Callable frontend code: To have a prebuilt chatbox that can be imported into websites code
Deployment: Employ efficient deployment strategies to make optimize cost and latency of the system, while using heavy models

 

Bag Of Word Implementation With Deployment 


A bag of words is a Natural Language Processing technique of text modeling. In technical terms, we can say that it is a method of feature extraction with text data. This approach is a simple and flexible way of extracting features from documents. It is called a “bag” of words because any information about the order or structure of words in the document is discarded. The model is only concerned with whether known words occur in the document, not wherein the document.
Training And Modeling Process

Advantages 
The lightweight model makes its low latency and fast
With enough data and proper model training, it can give a good response
Simpler system 

Disadvantage 
The use of TensorFlow and NLTK corpus enlarge the container
The answers are fixed for a given tag, hence feels mechanized
Shallow understanding of language
Not understand of context

BERT Based Question Answering Model

BERT (Bidirectional Encoder Representation from Transformer) is designed to pre-train deep bidirectional representations from the unlabeled text by jointly conditioning on both left and right contexts. 

It is pre-trained on a huge text corpus of millions of words and it can be fine-tuned by adding some extra layer to the output. 

A similar fine-tuned model is for the Question-Answering task on SQAuD Dataset. It takes in questions and the context as input to give out the index of answers in the context text. This can be further fine-tuned for a given task to get even better performance. 

Advantages
Deep understanding of language 
Wordpiece tokenization can handle any word elegantly 
Accurate answers from the given context and a high accuracy 
Very high understanding of context
Almost no training required

Disadvantages 
Heavy model 
Difficult to deploy 
High Cost and very high latency 
One word answers

Atttention Based Model 

Both BERT model and BOW model have their disadvantage. While BOW doesn’t understand the context, BERT model is very heavy and high computation. 

To get the best of both world, following changes were made to initial BOW model - 
Instead of lametisation of words with nltk, word embedding were extracted using spacy
Using BOW just checked if the word was present or not, while the context was missed. Getting an array of numbers per word, gives enough information for model to under context.
Instead of using dense network, a convolution and attention based architecture was created.
Since the word embedding were used means a grid like structure input which was a lot of data. 
Convolutional layers were taking the input to simplify the huge data followed by attention layer to better understand language context followed by dense layer. 
The idea of using fixed answer is also applied here. The dataloading and preprocessing steps changes. 


Advantage 
A model able to understand context better, while not being as heavy as BERT 
Efficient deployment with good performance 
Low latency 

Disadvantage
The model although not as complex, but needs huge amount of data to train from scratch
Model convergence is a issue, since its experimental 

Semantic Search 

The new attention based model needs huge data and training time computation. Semantic Search is a data searching technique in a which a search query aims to determine the intent and contextual meaning of the the words a person is using for search. 

Our implementation of semantic search has ability to query to n number of queries from k entries in one iteration. Given a GPU device, thousands of queries in millions of entries can happen in millisecond time frame. 

The embedding generation again uses BERT, given the bert-base it is computationally expensive and 512 array size does take substantial memory given many entries and time to compute. To deal with which, BertTiny with 90% MRR Score while being upto x20 faster. Shortening embedding length 256, also decreases the semantic search time. 

Advantages 
No model training required
Very fast 
It can be scaled to any volume given, the resources increase 


Disadvantage 
There is a need to manually create the entries, in this case question and answer sets. 
Due to fixed answers, it might sound less responsive 

Deployment 

Below are the options experimented to Deploy the BOW implementation -   
Communication protocols
Websocket - complex, though effective
Rest 
Server architecture
AWS Lambda - can’t deploy heavy models or text corpus
AWS EC2 - can deploy heavy models, though it’ll need a lot of other service like API gateway, Autoscaling and Loadbalancing to support performance.   
Individual api 
flask
Deployment strategies
Heroku 
Pythonanywhere
AWS
Docker - To containerize the app and to setup api on any port 


Below are the following methods to call a hosted API - 
User Interface and user experience problems with HTML and CSS
To call api 
AJAX - Problem related to CORS  
CURL 
FETCH
Callable module with just one line of code
Host the client side website


Future Scope 

To solve the problems of creating entries, we can use generative models to generate question-answer set.  
Though we have found multiple solution for querying, but there are still miles to go for conversational part of the project. 
 
