#%%writefile app.py
import streamlit as st
#import io
import random
import string
import nltk
import warnings
#import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from gtts import gTTS
import os
import playsound
from PIL import Image
warnings.filterwarnings('ignore')
import speech_recognition as sr 
import nltk
from nltk.stem import WordNetLemmatizer


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# for downloading package files can be commented after First run
# nltk.download('popular', quiet=True)
# nltk.download('nps_chat',quiet=True)
# nltk.download('punkt') 
# nltk.download('wordnet')

st.title("chatbot")

posts = nltk.corpus.nps_chat.xml_posts()[:10000]

# To Recognise input type as QUES. 
def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)

#colour palet
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))


#Reading in the input_corpus
with open('DeepsphereBotreply','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#Tokenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generating response and processing 
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

if st.button("Get your Assistant"):
    r1 = random.randint(1,10000000)
    r2 = random.randint(1,10000000)
    file = str(r2)+"randomtext"+str(r1) +".mp3"
    #Recording voice input using microphone 
    flag=True
    fst="Hello, i am your personal chatbot. I will answer your queries. If you want to exit, say Bye"
    tts = gTTS(fst,lang="en",tld="com")               
    tts.save(file)
    # os.system("mpg123 " + file )
    r = sr.Recognizer()
#     prYellow(fst)
    st.write(f'<p style="font-family: sans-serif;font-size: 15px;text-transform: capitalize;background-color: #d9d8d8;padding: 18px;border-radius: 15px">{fst}</p>', unsafe_allow_html=True)
    playsound.playsound(file,True)
    os.remove(file)

    # Taking voice input and processing 
    while(flag==True):
        with sr.Microphone(device_index=1) as source:
#             print("Say now!!!!")
            st.write("Listening...")
            audio= r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            user_response = format(r.recognize_google(audio))
#             print("\033[91m {}\033[00m" .format("YOU SAID : "+user_response))
            st.write(f'<p style="font-family: sans-serif;color: white;font-size: 15px;text-align:right;text-transform: capitalize;background-color: #190380;padding: 18px;border-radius: 15px">{user_response}</p>', unsafe_allow_html=True)
        except sr.UnknownValueError:
#             prYellow("Oops! Didn't catch that")
            st.write("Oops! Didn't catch that")
            pass

        
        # user_response = input()
        # user_response=user_response.lower()
        clas=classifier.classify(dialogue_act_features(user_response))
        if(clas!='Bye'):
            if(clas=='Emotion'):
                flag=False
#                 prYellow("Bot: You are welcome..")
                st.write("Bot: You are welcome..")
            else:
#                 if(greeting(user_response)!=None):
# #                     print("\033[93m {}\033[00m" .format("Bot: "+greeting(user_response)))
                    
#                 else:
#                     print("\033[93m {}\033[00m" .format("Bot: ",end=""))
                st.write("Bot:")
                res=(response(user_response))
#                 response.get("https://translate.google.com/", verify=False)
#                     prYellow(res)
                st.write(f'<p style="font-family: sans-serif;font-size: 15px;text-transform: capitalize;background-color: #d9d8d8;padding: 18px;border-radius: 15px">{res}</p>', unsafe_allow_html=True)
			
		#st.write(f'<p style="background-color:#7c7e86;color:#33ff33;font-size:24px;border-radius:2%;">res</p>',unsafe_allow_html=True)
                sent_tokens.remove(user_response)
                tts = gTTS(res,tld="com")
                tts.save(file)
                # os.system("mpg123 " + file)
                playsound.playsound(file,True)
                os.remove(file)
        else:
            flag=False
#             prYellow("Bot: Bye! take care..") 
            st.write("Bot: Bye! take care..")


# image1 = Image.open('logo.jpg')
# st.image(image1)

image2 = Image.open('robot.png')
st.image(image2)
