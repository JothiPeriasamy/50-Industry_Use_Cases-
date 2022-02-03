import json
import requests
import string
import re
import nltk
import string
import itertools
import streamlit as st
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
import pke
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import traceback
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import re
from pprint import pprint
import random
from prettytable import PrettyTable
from IPython.display import Markdown, display

@st.cache(show_spinner=False)
def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences

@st.cache(show_spinner=False)
def get_keywords(text):
    out=[]
    try:
        extractor = pke.unsupervised.YAKE()
        extractor.load_document(input=text)
        # pos = {'VERB', 'ADJ', 'NOUN'}
        pos ={'NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.candidate_selection(n=2,pos=pos, stoplist=stoplist)

        extractor.candidate_weighting(window=3,
                                      stoplist=stoplist,
                                      use_stems=False)

        keyphrases = extractor.get_n_best(n=30)
        
        for val in keyphrases:
            out.append(val[0])
    except:
        out = []
        traceback.print_exc()

    return out

#Extract sentences having the keywords that is extracted before.
@st.cache(show_spinner=False)
def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=False)
        keyword_sentences[key] = values
    return keyword_sentences


def sentence_answers(keyword_sentence_mapping):
    answers = []
    final_sentences = []
    for k,v in keyword_sentence_mapping.items():
        if len(v)>0:
            match = v[0].lower()
            answers.append(k)
            if k in match:
                temp = re.compile(re.escape(k), re.IGNORECASE)
                final_sentences.append(temp.sub('<answer>',match))
            else:
                final_sentences.append(match)
    return final_sentences, answers

def printmd(string):
    display(Markdown(string))

@st.cache(show_spinner=False)
@st.cache(allow_output_mutation=True)
def question(keyword_sentence_mapping):
    # tab = PrettyTable()
    answers, final_sentences = sentence_answers(keyword_sentence_mapping)
    random.shuffle(answers)
    random.shuffle(final_sentences)
    cols = {
        "A": answers,
        "B": final_sentences
    }
    # tab.field_names=['A', 'B']
    # tab.align["A"] = "l"
    # tab.align["B"] = "l"

    # # printmd('**Match column A with column B**')

    # for word,context in zip(answers,final_sentences):
    #     tab.add_row([word,context.replace("\n"," ")])
    #     tab.add_row(['',''])
    return cols
