import streamlit as st
import libs.utils as utils
import Main as main


st.set_page_config(page_title="News Summary", page_icon=":mailbox_with_mail:")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; '>News Summary</h1>", unsafe_allow_html=True)
utils.add_logo()
@st.cache_resource
def loading_news_model():
    path=main.App.config().get(section='PATH', option='NEWS_MODEL_PATH')
    with st.spinner('Loading Model...'):
        from transformers import pipeline
        pipe = pipeline('summarization', model=path)
    return pipe
newspipe = loading_news_model()

#Options

length_penalty = 1
num_beams = 8
max_char = 1024
@st.experimental_dialog("Summary")
def showdialog(a):
    st.write(a)


st.sidebar.header("Custom generation options:")
with st.sidebar:
    length_penalty = st.slider("Length penalty", 0.5, 1.0, 1.0, 0.1)
    num_beams = st.slider("Number of beams", 1, 10, 8)


txt = st.text_area("Input text for summary.")
progress_text = "Enter the text for summary."
submit_button = st.button(label="Summary", help="Click to Summary", use_container_width=True)

if txt != "":
    if submit_button:
        my_bar = st.progress(0, text=progress_text)

        my_bar.progress(0, text="Applying TF-IDF...")
        tfidf_txt = utils.TF_IDF_news(txt, max_char)
        my_bar.progress(50, text="Summarizing...")

        custom_dialogue=tfidf_txt
        gen_kwargs = {'length_penalty': length_penalty, 'num_beams': num_beams, 'use_cache':True}
        summary = newspipe(custom_dialogue, **gen_kwargs)
            
        my_bar.progress(100, text="Finish!")
        oldtext = summary[0]["summary_text"]
        showdialog(summary[0]["summary_text"])
    
else:
    st.error("Please enter text!")
