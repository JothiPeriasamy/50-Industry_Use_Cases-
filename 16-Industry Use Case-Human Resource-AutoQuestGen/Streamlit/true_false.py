import streamlit as st
from nltk import tokenize
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize
from allennlp.predictors.predictor import Predictor
import re
import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import nltk
nltk.download('punkt')

predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")

# Tokenizing sentence using nltk sent_tokenize
@st.cache
def tokenize_sentences_tf(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences[0]

# Method returns parts of speech tree for given sentence
@st.cache(show_spinner=False)
def pos_tree_from_sentence(text):
    sentence = tokenize_sentences_tf(text)
    sentence = sentence.rstrip('?:!.,;')
    parser_output = predictor.predict(sentence=sentence)
    tree_string = parser_output["trees"]
    tree = Tree.fromstring(tree_string)
    return tree






# split at right most nounphrase or verbphrase
@st.cache
def get_flattened(t):
    sent_str_final = None
    if t is not None:
        sent_str = [" ".join(x.leaves()) for x in list(t)]
        sent_str_final = [" ".join(sent_str)]
        sent_str_final = sent_str_final[0]
    return sent_str_final

@st.cache
def get_right_most_VP_or_NP(parse_tree,last_NP = None,last_VP = None):
    if len(parse_tree.leaves()) == 1:
        return last_NP,last_VP
    last_subtree = parse_tree[-1]
    if last_subtree.label() == "NP":
        last_NP = last_subtree
    elif last_subtree.label() == "VP":
        last_VP = last_subtree
    
    return get_right_most_VP_or_NP(last_subtree,last_NP,last_VP)


# sub_string - sipping coffee
# main_string - The old woman was sitting under a tree and sipping coffee
# compare like below
# Theoldwomanwassittingunderatreeandsippingcoffee  || sippingcoffee
# oldwomanwassittingunderatreeandsippingcoffee || sippingcoffee
# womanwassittingunderatreeandsippingcoffee || sippingcoffee
# ...............
# andsippingcoffee || sippingcoffee
# sippingcoffee || sippingcoffee
@st.cache
def get_termination_portion(main_string, sub_string):
    combined_sub_string = sub_string.replace(" ", "")
    main_string_list = main_string.split()
    last_index = len(main_string_list)
    for i in range(last_index):
        check_string_list = main_string_list[i:]
        check_string = "".join(check_string_list)
        check_string = check_string.replace(" ", "")
        if check_string == combined_sub_string:
            return " ".join(main_string_list[:i])

    return None




@st.cache(show_spinner=False)
def get_np_vp(tree,sentence):
    last_nounphrase, last_verbphrase =  get_right_most_VP_or_NP(tree)
    last_nounphrase_flattened = get_flattened(last_nounphrase)
    last_verbphrase_flattened = get_flattened(last_verbphrase)
    if last_nounphrase is not None and last_verbphrase is not None:
        longest_phrase_to_use = max(last_nounphrase_flattened, last_verbphrase_flattened)      
    elif last_nounphrase is not None:
        longest_phrase_to_use = last_nounphrase_flattened      
    elif last_verbphrase is not None:
        longest_phrase_to_use = last_verbphrase_flattened        
    else:
        print('-----------------Noun phrase & Verb Phrase both are None--------------------')
        print('noun phrase - ',last_nounphrase)
        print('verb phrase- ',last_verbphrase)
    longest_phrase_to_use = re.sub(r"-LRB- ", "(", longest_phrase_to_use)
    longest_phrase_to_use = re.sub(r" -RRB-", ")", longest_phrase_to_use)
    sentence = sentence.rstrip('?:!.,;')
    split_sentence = get_termination_portion(sentence, longest_phrase_to_use)
    return split_sentence








@st.cache(show_spinner=False)
def alternate_sentences(pos,sentence):
    GPT2tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    GPT2model = TFGPT2LMHeadModel.from_pretrained("gpt2",pad_token_id=GPT2tokenizer.eos_token_id)
#     GPT2tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
#     GPT2model = TFGPT2LMHeadModel.from_pretrained("distilgpt2",pad_token_id=GPT2tokenizer.eos_token_id)
    partial_sentence = get_np_vp(pos,sentence)
    input_ids = GPT2tokenizer.encode(partial_sentence,return_tensors='tf')
    maximum_length = len(partial_sentence.split())+40
    # Activate top_k sampling and top_p sampling with only from 90% most likely words
    sample_outputs = GPT2model.generate(
        input_ids, 
        do_sample=True, 
        max_length=maximum_length, 
        top_p=0.80, # 0.85 
        top_k=30,   #30
        repetition_penalty  = 10.0,
        num_return_sequences=10)
    generated_sentences=[]

    for i, sample_output in enumerate(sample_outputs):
        decoded_sentence = GPT2tokenizer.decode(sample_output, skip_special_tokens=True)
        # final_sentence = decoded_sentence
        final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
        generated_sentences.append(final_sentence)
    return generated_sentences


