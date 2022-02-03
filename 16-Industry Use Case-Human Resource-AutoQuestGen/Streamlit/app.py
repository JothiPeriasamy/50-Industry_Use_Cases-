  
import streamlit as st
import traceback
from PIL import Image
# Utils Pkgs
import codecs
import streamlit.components.v1 as stc
import textwrap
import pandas as pd
import base64
from datetime import datetime

from main import all_initialisations,fill_blank,true_false,mcq,match_the_foll


if __name__=='__main__':
    try:
        choice = all_initialisations()
        sentences= []
        noun_verbs_adj=[]
        keyword_sentence_mapping_noun_verbs_adj = {}
        if choice=='Fill in the Blanks':
            st.subheader(choice)
            fill_blank( sentences,noun_verbs_adj,keyword_sentence_mapping_noun_verbs_adj)
        if choice=='True or False':
            st.subheader(choice)
            true_false()
        if choice == 'Match the Following':
            st.subheader(choice)
            match_the_foll()
        if choice == 'MCQ':
            st.subheader('Multiple Choice Questions')
            mcq()
    except BaseException as e:
        print('error in main method - ',e)
        traceback.print_exc()
