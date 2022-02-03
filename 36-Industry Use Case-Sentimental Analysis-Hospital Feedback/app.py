#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import streamlit as st
from sentiment_analyzer import sentiment_analysis, get_noun, top_neg_word, frequency_counter
from text_preprocessing import clean_review
import pandas as pd
import io
import base64
import os
import json
import pickle
import uuid
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Patient Review Sentiment Analyzer")
def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            #object_to_download = object_to_download.to_csv(index=False)
            towrite = io.BytesIO()
            object_to_download = object_to_download.to_excel(towrite, encoding='utf-8', index=False, header=True)
            towrite.seek(0)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(towrite.read()).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{button_text}</a><br></br>'

    return dl_link

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding ='latin1')
    df.columns =['Reviews']
    list_text = df.Reviews.tolist()
    print(f'Total Number of Reviews : {len(list_text)}')
    analysis = sentiment_analysis(list_text)
    st.write(analysis)
    clean_text = []
    for text in list_text:
        text = clean_review(text)
        clean_text.append(text)
    textss = ' '.join(map(str, clean_text))
    
    filename = 'model_outcome.xlsx'
    download_button_str = download_button(analysis, filename, f'Click here to download {filename}', pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
    
    
    
    if st.checkbox("Wordcloud"):
        
        nouns = get_noun(clean_text)
        #only_neg = top_neg_word(clean_text)
        #print(f'Negative word: {top_neg_word(clean_text)}')
        #print(f'Cause of negativity: {nouns}')
        neg_words = ' '.join(map(str, nouns ))
        #only_neg_words = ' '.join(map(str, only_neg))
        fig, ax = plt.subplots()
        wordcloud =  WordCloud().generate(neg_words)
        plt.imshow(wordcloud,interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)
        
        
        
    if st.checkbox("Word Frequency Chart"):
        freq = frequency_counter(list_text)
        fig = px.bar(freq, x="count", y="word", height=1000)
        #fig, axes = plt.subplots(3,1,figsize=(8,20))
        st.plotly_chart(fig)        
        






