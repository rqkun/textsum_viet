import streamlit as st
import libs.utils as utils
import Main as main



@st.experimental_dialog("Summary")
def showdialog(a):
    st.write(a)

st.set_page_config(page_title="Laws Summary", page_icon=":notebook:")
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; '>Law Summary</h1>", unsafe_allow_html=True)
utils.add_logo()

@st.cache_resource
def loading_news_model():
    path=main.App.config().get(section='PATH', option='LAWS_MODEL_PATH')
    with st.spinner('Loading Model...'):
        from transformers import pipeline
        pipe = pipeline('summarization', model=path)
    return pipe
lawspipe = loading_news_model()

#OPTIONS
length_penalty = 1
num_beams = 8
max_char = 1024
#SIDE
st.sidebar.header("Custom generation options:")
with st.sidebar:
    length_penalty = st.slider("Length penalty", 0.5, 1.0, 1.0, 0.1)
    num_beams = st.slider("Number of beams", 1, 10, 8)
#MAIN
txt = st.text_area("Input text",label_visibility="collapsed")
progress_text = "Enter the text for summary."

col1,col2=st.columns(2)
with col1:
    my_bar = st.progress(0, text=progress_text)
with col2:
    formbtn = st.button("Submit",use_container_width=True,type="primary")

if "formbtn_state" not in st.session_state:
    st.session_state.formbtn_state = False

if formbtn or st.session_state.formbtn_state:
    st.session_state.formbtn_state = True
    if txt != "":
        with st.form(key = 'choice'):
            dieu_dict = utils.create_Dict(txt)
            if (len(dieu_dict) >0):
                btns=[]
                for key, val in dieu_dict.items():
                    btns.append(key)
                genre = st.radio("Which part to summarize: ", btns)
                submit_form = st.form_submit_button(label="Summary", help="Click to Summary", use_container_width=True)
                if submit_form:
                    source = dieu_dict.get(genre)
                    my_bar.progress(0, text="Applying TF-IDF...")

                    tfidf_txt = utils.TF_IDF(source, max_char)
                    my_bar.progress(50, text="Summarizing...")

                    custom_dialogue=tfidf_txt
                    gen_kwargs = {'length_penalty': length_penalty, 'num_beams': num_beams, 'use_cache':True}
                    summary = lawspipe(custom_dialogue, **gen_kwargs)

                    my_bar.progress(100, text="Finish!")
                    showdialog(summary[0]["summary_text"])
            else:
                my_bar.progress(0, text="Applying TF-IDF...")

                tfidf_txt = utils.TF_IDF(txt, max_char)
                my_bar.progress(50, text="Summarizing...")

                custom_dialogue=tfidf_txt
                gen_kwargs = {'length_penalty': length_penalty, 'num_beams': num_beams, 'use_cache':True}
                summary = lawspipe(custom_dialogue, **gen_kwargs)

                my_bar.progress(100, text="Finish!")
                showdialog(summary[0]["summary_text"])
    else:
        st.error("Please enter text!")
