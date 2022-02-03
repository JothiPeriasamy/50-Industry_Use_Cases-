import json
import requests
import string
import re
import nltk
import string
import itertools
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt') 
import pke
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import traceback
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from sense2vec import Sense2Vec
from collections import OrderedDict
import random
from transformers import T5ForConditionalGeneration,T5Tokenizer
import streamlit as st

# If we want to perform MCQ - we need below files/libraries
# !pip install --quiet sense2vec==1.0.2
# !wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
# !tar -xvf  s2v_reddit_2015_md.tar.gz

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
# @st.cache(allow_output_mutation=True)
def sense2vec_get_words(word):
    s2v = Sense2Vec().from_disk('s2v_old')
    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=20)
    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word.lower():
            output.append(append_word.title())

    out = list(OrderedDict.fromkeys(output))
    return out

# @st.cache(show_spinner=False)
# @st.cache(allow_output_mutation=True)
def kw_distractors(keyword_list):
    distr = {}
    for kw in keyword_list:
        distractors = sense2vec_get_words(kw)
        if len(distractors)>=3:
            distr[kw] = random.sample(distractors,3)
            distr[kw].append(kw)
        elif len(distractors) >= 1 and len(distractors) < 3:
            distr[kw] = distractors
            distr[kw].append(kw)
        else:
            distr[kw] = []
    return distr

#Generate a question using context and answer with T5
def get_question(sentence,answer):
    question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
    question_tokenizer = T5Tokenizer.from_pretrained('t5-base')
    text = "context: {} answer: {} </s>".format(sentence,answer)
    max_len = 256
    encoding = question_tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=True, return_tensors="pt")

    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outs = question_model.generate(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    early_stopping=True,
                                    num_beams=5,
                                    num_return_sequences=1,
                                    no_repeat_ngram_size=2,
                                    max_length=200)

    dec = [question_tokenizer.decode(ids) for ids in outs]


    Question = dec[0].replace("question:","")
    Question= Question.strip()
    return Question

# @st.cache(show_spinner=False)
# @st.cache(allow_output_mutation=True)
def getMCQ(keyword_sentence_mapping,choices):
    ques = {}
    for k,v in keyword_sentence_mapping.items():
        sentence_for_T5 = " ".join(random.sample(v,1)[0].split()) 
        ques[k] = get_question(sentence_for_T5,k)
    count = 1
    final_out = {v:choices[k] for k,v in ques.items()}
    return final_out