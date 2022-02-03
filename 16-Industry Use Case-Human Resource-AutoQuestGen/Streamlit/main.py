import streamlit as st
import traceback
from PIL import Image
# Utils Pkgs
import textwrap
import pandas as pd
import base64
from datetime import datetime
from nltk.tokenize import sent_tokenize

from true_false import  pos_tree_from_sentence,get_np_vp,alternate_sentences
from fill_blank import get_noun_adj_verb,get_sentences_for_keyword,get_fill_in_the_blanks
from matchthefollowing import  get_keywords,get_sentences_for_keyword,question
from mcq import get_keywords, get_sentences_for_keyword, kw_distractors, getMCQ

def file_selector():
    file = st.file_uploader('Upload the text file',type=['txt'])
    if file is not None:
        text = file.read().decode("utf-8")
        st.write('Selected file content is `%s`' % text)
        return text

def dtime():
      return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    
# Tokenizing sentence using nltk sent_tokenize
@st.cache(show_spinner=False)
def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences    
    
def output_file(out, quest_type):
      with open("output.txt","a",encoding="utf-8") as f:
        if quest_type == "Input Text":
              f.write("="*100+"\n")
        else:
              f.write("-"*100+"\n")
        dt = dtime()
        f.write(f"{dt} {quest_type}:\n")
        f.write("-"*100+"\n\n")
        if quest_type == "Match the Following":
            df = pd.DataFrame(out)
            df.to_string(f,index = False, justify="justify-all")
            f.write("\n")
        elif quest_type == "Input Text":
            f.write(f"{out}")
        elif quest_type == "Fill in The Blanks":
            for i,sent in enumerate(out["sentences"]):
                f.write(f"{str(i+1)}. {sent}\n")
            f.write("\n"+str(out["keys"])+"\n")
        elif quest_type == "MCQ":
            count = 1
            for quest,options in out.items():
                asci = 97
                f.write(f"{str(count)}. {quest}")
                if options:
                    for opt in options:
                        f.write(chr(asci)+")"+opt.capitalize()+" ")
                        asci += 1
                    f.write("\n")
                count += 1
        else:
            for i,que in enumerate(out):
                f.write(f"{str(i+1)}. {que}\n")
        f.write("\n")
        
        
        
        
        
        
        
        
        
def download_link(object_to_download, download_filename, download_link_text,quest_type):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
#     if isinstance(object_to_download,pd.DataFrame):
#         object_to_download = object_to_download.to_csv(index=False)
#     object_to_download = str(object_to_download)
    object_to_download1 = ""
    if quest_type == "Input Text":
        object_to_download1 = "="*100+"\r\n"
    else:
        object_to_download1 = "-"*100+"\r\n"
    dt = dtime()
    object_to_download1+=f"{dt} {quest_type}:\r\n"
    object_to_download1+="-"*100+"\r\n\r\n"
    if quest_type == "Match the Following":
        df = pd.DataFrame(object_to_download)
        df.to_string(download_filename,index = False, justify="justify-all")
        object_to_download1+=f"{df}\r\n"
    elif quest_type == "Input Text":
            object_to_download1+=f"{object_to_download}"
    elif quest_type == "Fill in The Blanks":
        for i,sent in enumerate(object_to_download["sentences"]):
            object_to_download1+=f"{str(i+1)}. {sent}\r\n"
        object_to_download1+="\n"+str(object_to_download["keys"])+"\r\n"
    elif quest_type == "MCQ":
            count = 1
            for quest,options in object_to_download.items():
                asci = 97
                object_to_download1+=f"{str(count)}. {quest}"
                if options:
                    for opt in options:
                        object_to_download1+=chr(asci)+")"+opt.capitalize()+" "
                        asci += 1
                    object_to_download1+=f"\r\n"
                count += 1
    else:
        for i,que in enumerate(object_to_download):
            object_to_download1+=f"{str(i+1)}. {que}\r\n"
    object_to_download1+=f"\r\n"
    b64 = base64.b64encode(object_to_download1.encode()).decode()
    
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    
        
        
        
        
        
        
        
        

def match_the_foll():
    text = file_selector()
    quest = "Match the Following"
    ts_col1,ts_col2,ts_col3 = st.beta_columns((1,1,2))
    ts_col1.success("Run Model")
    ts_col2.success("Step 1")
    if ts_col3.button('Tokenize sentences'):
        if text is not None:
            with st.spinner("Processing input to tokenize sentence"):
                sentences = tokenize_sentences(text)
                st.write(sentences)
            st.success('Tokenizing completed ')
        else:
            st.error("Please select input file!")
    ek_col1,ek_col2,ek_col3 = st.beta_columns((1,1,2))
    ek_col1.success("Run Model")
    ek_col2.success("Step 2")
    if ek_col3.button('Extract Keywords'):
        if text is not None:
            with st.spinner("Processing input to extract keywords"):
                keywords = get_keywords(text)[:6]
                st.write(keywords)
            st.success('Keywords Extracted')
        else:
            st.error("Please select input file!")
    km_col1,km_col2,km_col3 = st.beta_columns((1,1,2))
    km_col1.success("Run Model")
    km_col2.success("Step 3")
    if km_col3.button('Sentence Keyword Match'):
        if text is not None:
            with st.spinner("Processing input to match keywords with sentences"):
                sentences = tokenize_sentences(text)
                keywords = get_keywords(text)[:6]
                keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
                st.write(keyword_sentence_mapping)
            st.success('Sentence Keyword Match Completed')
        else:
            st.error("Please select input file!")
    fq_col1,fq_col2,fq_col3 = st.beta_columns((1,1,2))
    fq_col1.success("Run Model")
    fq_col2.success("Step 4")
    if fq_col3.button('Match the Following Questions'):
        if text is not None:
            with st.spinner("Processing input to generate questions"):
                sentences = tokenize_sentences(text)
                keywords = get_keywords(text)[:6]
                keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
                mtf_table= question(keyword_sentence_mapping)
                # st.write(mtf_table)
                st.table(mtf_table)
                output_file(text,"Input Text")
                output_file(mtf_table, quest)
        else:
            st.error("Please select input file!")
    vm_col1,vm_col2,vm_col3 = st.beta_columns((1,1,2))
    vm_col1.success("Validate Model")
    vm_col2.success("Step 5")
    if vm_col3.button('View Model Outcome'):
        if text is not None:
            sentences = tokenize_sentences(text)
            keywords = get_keywords(text)[:6]
            keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
            mtf_table = question(keyword_sentence_mapping)
            st.markdown(download_link(mtf_table, 'model_output.txt', 'Click here to download your output!',quest),unsafe_allow_html=True)
        else:
            st.error("Please select input file!")

def mcq():
    text = file_selector()
    quest = "MCQ"
    ts_col1,ts_col2,ts_col3 = st.beta_columns((1,1,2))
    ts_col1.success("Run Model")
    ts_col2.success("Step 1")
    if ts_col3.button('Tokenize sentences'):
        if text is not None:
            with st.spinner("Processing input to tokenize sentence"):
                sentences = tokenize_sentences(text)
                st.write(sentences)
            st.success('Tokenizing completed ')
        else:
            st.error("Please select input file!")
    ek_col1,ek_col2,ek_col3 = st.beta_columns((1,1,2))
    ek_col1.success("Run Model")
    ek_col2.success("Step 2")
    if ek_col3.button('Extract Keywords'):
        if text is not None:
            with st.spinner("Processing input to extract keywords"):
                keywords = get_keywords(text)[:6]
                st.write(keywords)
            st.success('Keywords Extracted')
        else:
            st.error("Please select input file!")
    km_col1,km_col2,km_col3 = st.beta_columns((1,1,2))
    km_col1.success("Run Model")
    km_col2.success("Step 3")
    if km_col3.button('Sentence Keyword Match'):
        if text is not None:
            with st.spinner("Processing input to match keywords with sentences"):
                sentences = tokenize_sentences(text)
                keywords = get_keywords(text)[:6]
                keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
                st.write(keyword_sentence_mapping)
            st.success('Sentence Keyword Match Completed')
        else:
            st.error("Please select input file!")
    fq_col1,fq_col2,fq_col3 = st.beta_columns((1,1,2))
    fq_col1.success("Run Model")
    fq_col2.success("Step 4")
    if fq_col3.button('Multiple Choice Questions'):
        if text is not None:
            with st.spinner("Processing input to generate questions"):
                sentences = tokenize_sentences(text)
                keywords = get_keywords(text)[:6]
                keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
                choices = kw_distractors(keywords)
                mcq_ques = getMCQ(keyword_sentence_mapping,choices)
                st.write(mcq_ques)
                output_file(text,"Input Text")
                output_file(mcq_ques, quest)
        else:
            st.error("Please select input file!")
    vm_col1,vm_col2,vm_col3 = st.beta_columns((1,1,2))
    vm_col1.success("Validate Model")
    vm_col2.success("Step 5")
    if vm_col3.button('View Model Outcome'):
        if text is not None:
            sentences = tokenize_sentences(text)
            keywords = get_keywords(text)[:6]
            keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)
            mtf_table = question(keyword_sentence_mapping)
            st.markdown(download_link(mtf_table, 'model_output.txt', 'Click here to download your output!',quest),unsafe_allow_html=True)
        else:
            st.error("Please select input file!")


def fill_blank(sentence,noun_verbs_adj,keyword_sentence_mapping_noun_verbs_adj):
    text = file_selector()
    quest = "Fill in The Blanks"
    ts_col1,ts_col2,ts_col3 = st.beta_columns((1,1,2))
    ts_col1.success("Run Model")
    ts_col2.success("Step 1")
    if ts_col3.button('Tokenize sentences'):
        if text is not None:
            with st.spinner("Processing input to tokenize sentence"):
                sentences = tokenize_sentences(text)
                st.write(sentences)
            st.success('Tokenizing completed ')
        else:
            st.error("Please select input file!")
    ek_col1,ek_col2,ek_col3 = st.beta_columns((1,1,2))
    ek_col1.success("Run Model")
    ek_col2.success("Step 2")
    if ek_col3.button('Extract Keywords'):
        if text is not None:
            with st.spinner("Processing input to extract keywords"):
                noun_verbs_adj = get_noun_adj_verb(text)
                st.write(noun_verbs_adj)
            st.success('Keywords Extracted')
        else:
            st.error("Please select input file!")
    sk_col1,sk_col2,sk_col3 = st.beta_columns((1,1,2))
    sk_col1.success("Run Model")
    sk_col2.success("Step 3")
    if sk_col3.button('Sentence Keyword Match'):
        if text is not None:
            with st.spinner("Processing input to match keywords with sentences"):
                sentences = tokenize_sentences(text)
                noun_verbs_adj = get_noun_adj_verb(text)
                keyword_sentence_mapping_noun_verbs_adj = get_sentences_for_keyword(noun_verbs_adj, sentences)
                st.write(keyword_sentence_mapping_noun_verbs_adj)
            st.success('Sentence Keyword Match Completed')
        else:
            st.error("Please select input file!")
    fb_col1,fb_col2,fb_col3 = st.beta_columns((1,1,2))
    fb_col1.success("Run Model")
    fb_col2.success("Step 4")
    if fb_col3.button('Fill in the Blank Questions'):
        if text is not None:
            with st.spinner("Processing input to generate Fill in the blank questions"):
                sentences = tokenize_sentences(text)
                noun_verbs_adj = get_noun_adj_verb(text)
                keyword_sentence_mapping_noun_verbs_adj = get_sentences_for_keyword(noun_verbs_adj, sentences)
                fill_in_the_blanks = get_fill_in_the_blanks(keyword_sentence_mapping_noun_verbs_adj)
                st.write(fill_in_the_blanks)
                output_file(text,"Input Text")
                output_file(fill_in_the_blanks, quest)
        else:
            st.error("Please select input file!")
    vm_col1,vm_col2,vm_col3 = st.beta_columns((1,1,2))
    vm_col1.success("Validate Model")
    vm_col2.success("Step 5")
    if vm_col3.button('View Model Outcome'):
        if text is not None:
            sentences = tokenize_sentences(text)
            noun_verbs_adj = get_noun_adj_verb(text)
            keyword_sentence_mapping_noun_verbs_adj = get_sentences_for_keyword(noun_verbs_adj, sentences)
            fill_in_the_blanks = get_fill_in_the_blanks(keyword_sentence_mapping_noun_verbs_adj)
            st.markdown(download_link(fill_in_the_blanks, 'model_output.txt', 'Click here to download your output!',quest),unsafe_allow_html=True)
        else:
            st.error("Please select input file!")

                
def true_false():
    text = file_selector()
    quest = "True or False"
    ts_col1,ts_col2,ts_col3 = st.beta_columns((1,1,2))
    ts_col1.success("Run Model")
    ts_col2.success("Step 1")
    if ts_col3.button('Tokenize sentences'):
        if text is not None:
            with st.spinner("Processing input to tokenize sentence and get 1st sentence to generate question"):
                sentences = tokenize_sentences(text)[0]
                st.write(sentences)
            st.success('Generated first sentence from given input')
        else:
            st.error("Please select input file!")
    wc_col1,wc_col2,wc_col3 = st.beta_columns((1,1,2))
    wc_col1.success("Run Model")
    wc_col2.success("Step 2")
    if wc_col3.button('Words Construction'):
        if text is not None:
            with st.spinner("Parsing input to construct words"):
                sentences = tokenize_sentences(text)[0]
                pos = pos_tree_from_sentence(text)
                st.write(pos)
            st.success('Grammatical parsing completed')
        else:
            st.error("Please select input file!")
    sc_col1,sc_col2,sc_col3 = st.beta_columns((1,1,2))
    sc_col1.success("Run Model")
    sc_col2.success("Step 3")
    if sc_col3.button('Sentence Construction'):
        if text is not None:
            with st.spinner("Splitting sentence in-progress"):
                sentences = tokenize_sentences(text)[0]
                pos = pos_tree_from_sentence(text)
                split_sentence = get_np_vp(pos,sentences)
                print('split_sentence in app.py- ',split_sentence)
                st.write(split_sentence)
            st.success('Sentence splitted')
        else:
            st.error("Please select input file!")
    as_col1,as_col2,as_col3 = st.beta_columns((1,1,2))
    as_col1.success("Run Model")
    as_col2.success("Step 4")
    if as_col3.button('Alternate Sentences'):
        if text is not None:
            with st.spinner("Generating Alternate sentences"):
                sentences = tokenize_sentences(text)[0]
                pos = pos_tree_from_sentence(text)
                alt_sentence = alternate_sentences(pos,sentences)
                st.write(alt_sentence)
                output_file(text,"Input Text")
                output_file(alt_sentence,quest)
        else:
            st.error("Please select input file!")
    vm_col1,vm_col2,vm_col3 = st.beta_columns((1,1,2))
    vm_col1.success("Validate Model")
    vm_col2.success("Step 5")
    if vm_col3.button('View Model Outcome'):
        if text is not None:
            sentences = tokenize_sentences(text)[0]
            pos = pos_tree_from_sentence(text)
            alt_sentence = alternate_sentences(pos,sentences)
            st.markdown(download_link(alt_sentence, 'model_output.txt', 'Click here to download your output!',quest),unsafe_allow_html=True)
        else:
            st.error("Please select input file!")
    
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
def all_initialisations():
    local_css("style.css")
    image = Image.open('DeepSphere_Logo_Final.png')
    st.image(image)
    
    st.markdown('<h2>NLP Simplifies Questions and Assignments Construction <br><font style="color: #5500FF;">Powered by Google Cloud & Colab</font></h2>',unsafe_allow_html=True)
    st.markdown('<hr style="border-top: 6px solid #8c8b8b; width: 150%;margin-left:-180px">',unsafe_allow_html=True)
    activities= ['Select Your Question Type','Fill in the Blanks','True or False', 'Match the Following', 'MCQ']
    model_choices = ['Model Implemented','BERT']
    libraries = ['Library Used','spacy','nltk','tensorflow','allennlp','flashtext','streamlit','pke']
    gcp = ['GCP Services Used','VM Instance','Compute Engine']
    choice = st.sidebar.selectbox('',activities)
    model_choice = st.sidebar.selectbox('',model_choices)
    libraries_choice = st.sidebar.selectbox('',libraries)
    gcp_services = st.sidebar.selectbox('',gcp)
    return choice