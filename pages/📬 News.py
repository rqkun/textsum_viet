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

# You can also use "with" notation:
st.sidebar.header("Custom generation options:")
with st.sidebar:
    length_penalty = st.slider("Length penalty", 0.5, 1.0, 1.0, 0.1)
    num_beams = st.slider("Number of beams", 1, 10, 8)


txt = st.text_area("Input text",label_visibility="collapsed")
progress_text = "Enter the text for summary."
col1,col2=st.columns(2)
with col1:
    my_bar = st.progress(0, text=progress_text)
with col2:
    sumbt = st.button("Submit",use_container_width=True,type="primary")
if sumbt:
    if txt != "":
        my_bar.progress(0, text="Applying TF-IDF...")
        tfidf_txt = utils.TF_IDF(txt, max_char)
        my_bar.progress(50, text="Summarizing...")

        custom_dialogue=tfidf_txt
        gen_kwargs = {'length_penalty': length_penalty, 'num_beams': num_beams, 'use_cache':True}
        summary = newspipe(custom_dialogue, **gen_kwargs)
            
        my_bar.progress(100, text="Finish!")
        oldtext = summary[0]["summary_text"]
        showdialog(summary[0]["summary_text"])
        
    else:
        st.error("Please enter text!")

st.divider()
@st.experimental_fragment
def fragment():
    with st.spinner('Loading recent news...'):
        import time
        ucol1,ucol2,ucol3,ucol4= st.columns(4)
        time.sleep(2)
        with ucol1:
            st.image('https://i.imgur.com/pt3bm6Ml.png',use_column_width="always", caption='Sunrise by the mountains')
            st.link_button("Go","https://google.com",use_container_width=True)
        time.sleep(2)
        with ucol2:
            st.image('https://i.imgur.com/pt3bm6Ml.png',use_column_width="always", caption='Sunrise by the mountains')
            st.link_button("Go","https://google.com",use_container_width=True)
        time.sleep(2)
        with ucol3:
            st.image('https://i.imgur.com/pt3bm6Ml.png',use_column_width="always", caption='Sunrise by the mountains')
            st.link_button("Go","https://google.com",use_container_width=True)
        time.sleep(2)
        with ucol4:
            st.image('https://i.imgur.com/pt3bm6Ml.png',use_column_width="always", caption='Sunrise by the mountains')
            st.link_button("Go","https://google.com",use_container_width=True)

fragment()