#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import pandas as pd
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.toktok import ToktokTokenizer
from text_preprocessing import clean_review
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from collections import Counter


# In[2]:

model = joblib.load(open('model_nb.pkl', 'rb'))
cv = joblib.load(open('cv.pkl', 'rb'))

# In[3]:

sentiment_map = {'Negative':0, 'Positive':1}

# In[6]:

tokenizer = ToktokTokenizer()
sia = SentimentIntensityAnalyzer()

# In[7]:

def get_sentiment(text):
    """
    Predicts the sentiment of text using the Multinomial Naive Bayes Model
    """
    sentiment_id = model.predict(cv.transform([text]).toarray())
    return get_name(sentiment_id)

# In[8]:

def get_name(sentiment_id):
    """
    Gets sentiment name from sentiment_map using sentiment_id
    """
    for sentiment, id_ in sentiment_map.items():
        if id_ == sentiment_id:
            return sentiment

# In[9]:

def get_noun(text):
    """
    Finds noun of the text
    """
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)    
    pos_tags = nltk.pos_tag(tokens)
    nouns = []
    for word, tag in pos_tags:
        if tag == "NN" or tag == "NNP" or tag == "NNS":
            nouns.append(word)
    return nouns


# In[10]:


def get_tokens(text):
    """
    Converts text to a list of tokens using nltk tokenizer
    """
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


# In[11]:


def top_pos_word(text):
    """
    Finds top positive word using nltk vader library
    """
    pos_polarity = dict()
    for word in get_tokens(text):
        pos_score = sia.polarity_scores(word)['pos']
        if word not in pos_polarity:
            pos_polarity[word] = pos_score
        else:
            pos_polarity[word] += pos_score
    top_word = max(pos_polarity, key=pos_polarity.get)
    return top_word


# In[12]:


def top_neg_word(text):
    """
    Finds top negative word using nltk vader library
    """
    neg_polarity = dict()
    for word in get_tokens(text):
        neg_score = sia.polarity_scores(word)['neg']
        if word not in neg_polarity:
            neg_polarity[word] = neg_score
        else:
            neg_polarity[word] += neg_score
    top_word = max(neg_polarity, key=neg_polarity.get)
    return top_word

def frequency_counter(sentence):
    sentence =" ".join(sentence)
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    #counts the words, pairs and trigrams
    counted = Counter(new_tokens)
    #print(counted)
    word_freq = pd.DataFrame(counted.items(),columns=['word','count']).sort_values(by='count',ascending=False)
    #print(word_freq)
    return word_freq

# In[15]:

def sentiment_analysis(texts):
    """
    Finds the sentiment of text, sentiment score of cleaned text 
    and stores the result to dataframe
    
    """
    sentiment_list = []
    vader_score = []
    for text in texts:
        text = clean_review(text)
        print(f'Cleaning Reviews ............')
        sentiment = get_sentiment(text)
        print(f'Classified Sentiment for the review :{sentiment}')
        sentiment_list.append(sentiment)
        sid_obj = SentimentIntensityAnalyzer() 
        sentiment_dict = sid_obj.polarity_scores(text) 
        vader_score.append(sentiment_dict["compound"])
        #print(vader_score)
        
        #print(f'Sentiment: {sentiment}')
        
    pred_dict = {'Reviews':texts, 'Sentiment':sentiment_list,'Sentiment_Score':vader_score}
    pred_data = pd.DataFrame(pred_dict,columns=['Reviews','Sentiment','Sentiment_Score'])
    pred_data['Ranking'] = pred_data['Sentiment_Score'].rank(ascending = 1) # rank based on sentiment score
    pred_data['Ranking'] = pred_data['Ranking'].apply(int)
    pred_data.sort_values("Ranking", inplace = True)
    pred_data.drop('Sentiment_Score',axis=1,inplace=True)
    return pred_data






