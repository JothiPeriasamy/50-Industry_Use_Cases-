#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import string
import re
import nltk
from bs4 import BeautifulSoup
import unicodedata
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords, wordnet
import contractions
from nltk import pos_tag
from textblob import TextBlob
import joblib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# In[2]:


#remove html tags 
def strip_html_tag(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


# In[3]:


# remove accented characters
def strip_accents(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


# In[4]:


# remove special characters
def strip_special_characters(text):
    text = re.sub('[^a-zA-z0-9\s]', '', text)
    return text


# In[6]:


# expand contractions
def expand_contraction(text):
    text = contractions.fix(text)
    return text


# In[7]:


#pos tagging
def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# In[8]:


# main function to clean text
def clean_review(text):
    #remove html tags
    text = strip_html_tag(text)

    #convert accented characters
    text = strip_accents(text)
  
    #expand contractions
    text = expand_contraction(text)

    #lower case 
    text = text.lower()
    
    #remove special characters
    text = strip_special_characters(text)

    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]

    # remove stop words
    stopword_list = (stopwords.words('english'))
    stopword_list.remove('not')
    stopword_list.remove('no')
    stopword_list.append('dr')
  
    text = [x for x in text if x not in stopword_list]
 
    # pos tag text
    pos_tags = pos_tag([word for word in text if word])

    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]

    text = " ".join(text)
    return(text)


# In[ ]:




