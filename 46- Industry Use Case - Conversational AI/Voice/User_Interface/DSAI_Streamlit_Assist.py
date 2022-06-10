import streamlit as st
import random
import string
import nltk
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from gtts import gTTS
import os
import playsound
from PIL import Image
import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow import keras
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
# for downloading package files can be commented after First run
#nltk.download('popular', quiet=True)
#nltk.download('nps_chat',quiet=True)
#nltk.download('punkt') 
#nltk.download('wordnet')

def local_css(vAR_file_name):
    #function to apply style formatting from styles.css file in streamlit
    #filename - css file contains webpage formatting options
        with open(vAR_file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./style.css") #function call to load .css file and apply in streamlit webpage

vAR_col1, vAR_col2, vAR_col3 = st.columns([1,1,1])
vAR_col2.image('./DSAI_Logo.jpg', use_column_width=True)

st.title("Voice Based Chatbot") #set title for webpage

model = keras.models.load_model('../Utility/chat_model.h5')# load model

with open('../Utility/tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

with open('../Utility/label_encoder.pickle', 'rb') as f:
    lbl_encoder = pickle.load(f)

with open('../Utility/DSAI_Intents.json') as file:
    data = json.load(file)

# parameters
max_len = 20



def chat():
    # method to chat with robot
    vAR_r1 = random.randint(1,10000000)
    vAR_r2 = random.randint(1,10000000)
    vAR_file = str(vAR_r2)+"randomtext"+str(vAR_r1) +".mp3" #generate random file name

    #Recording voice input using microphone 
    fst="Hello"
    vAR_tts = gTTS(fst,lang="en",tld="com") #google text to speech API to convert the message to audio
    vAR_tts.save(vAR_file) #save the audio with the random filename generated

    vAR_r = sr.Recognizer() #recognize user input
    st.write(f'<p style="font-family: sans-serif;font-size: 15px;text-transform: capitalize;background-color: #190380;padding: 18px;border-radius: 15px">{fst}</p>', unsafe_allow_html=True)
    playsound.playsound(vAR_file,True) #play the bot reply
    os.remove(vAR_file) #remove the file generated

    # Taking voice input and processing
    tag = ''
    while(tag!='goodbye'):
        with sr.Microphone(device_index=1) as source: #microphone as input device
            st.write("Listening...")
            vAR_audio= vAR_r.adjust_for_ambient_noise(source)
            vAR_audio = vAR_r.listen(source)
        try:
            vAR_user_response = format(vAR_r.recognize_google(vAR_audio))
            st.write(f'<p style="font-family: sans-serif;color: white;font-size: 15px;text-align:right;text-transform: capitalize;background-color: #190380;padding: 18px;border-radius: 15px">{vAR_user_response}</p>', unsafe_allow_html=True)

            t = tokenizer.texts_to_sequences([vAR_user_response])
            p = pad_sequences(t, truncating='post', maxlen=max_len)
            result = model.predict(p)
            pred_class = np.argmax(result)
            tag = lbl_encoder.inverse_transform([pred_class])

            for i in data['intents']:
                if i['tag'] == tag:
                    resp = np.random.choice(i['responses'])

        except sr.UnknownValueError:
            resp = "Oops! Didn't catch that"

        st.write("Bot:")
        #st.write(resp)
        st.write(f'<p style="font-family: sans-serif;font-size: 15px;text-transform: capitalize;background-color: #190380;padding: 18px;border-radius: 15px">{resp}</p>', unsafe_allow_html=True)
        vAR_tts = gTTS(resp,tld="com")
        vAR_tts.save(vAR_file)
        playsound.playsound(vAR_file,True)
        os.remove(vAR_file)

'''                    
            if(vAR_clas!='Bye'):
                if(vAR_clas=='Emotion'):
                    vAR_flag=False
                    st.write("Bot: You are welcome..")
                else:
                    st.write("Bot:")
                    vAR_res=(self.response(vAR_user_response))
                    st.write(f'<p style="font-family: sans-serif;font-size: 15px;text-transform: capitalize;background-color: #d9d8d8;padding: 18px;border-radius: 15px">{vAR_res}</p>', unsafe_allow_html=True)
                    self.vAR_sent_tokens.remove(vAR_user_response)
                    vAR_tts = gTTS(vAR_res,tld="com")
                    vAR_tts.save(vAR_file)
                    playsound.playsound(vAR_file,True)
                    os.remove(vAR_file)
            else:
                vAR_flag=False
                st.write("Bot: Bye! take care..")
        except sr.UnknownValueError:
            st.write("Oops! Didn't catch that")
            pass'''

if st.button("Get your Assistant"): #event listener for 'Get your Assistant' button
    chat()

image2 = Image.open('../User_Interface/DSAI_Robot.png')
st.image(image2)