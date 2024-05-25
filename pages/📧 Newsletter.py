import streamlit as st
import libs.utils as utils
import Main as main
import math

st.set_page_config(page_title="Newsletter", page_icon=":e-mail:")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; '>Newsletter</h1>", unsafe_allow_html=True)
utils.add_logo()
@st.cache_resource
def loading_news_model():
    path=main.App.config().get(section='PATH', option='NEWS_MODEL_PATH')
    with st.spinner('Loading Model...'):
        from transformers import pipeline
        pipe = pipeline('summarization', model=path)
    return pipe

@st.cache_resource
def loadnews():
    recent_news_df=utils.get_latest_news()
    return recent_news_df

newspipe = loading_news_model()

#Options

length_penalty = 1
num_beams = 8
max_char = 1024
@st.experimental_dialog("Summary")
def showdialog(a):
    st.write(a)

recent_news_df = loadnews()
with st.spinner('Loading recent news...'):
    for i in range(len(recent_news_df['abstract'])):
        gen_kwargs2 = {'length_penalty': 1, 'num_beams': num_beams}
        tdf  = utils.TF_IDF_news(recent_news_df['content'][i], max_char)
        tmp = newspipe(tdf, **gen_kwargs2)
        img = recent_news_df['image_url'][i]
        if img is None or img == "":
            img = "https://i.imgur.com/pt3bm6Ml.png"
        st.image(img ,use_column_width="always", caption=tmp[0]["summary_text"])
        st.link_button("Go",recent_news_df['link'][i],use_container_width=True,help=recent_news_df['abstract'][i])
        st.divider()
    
