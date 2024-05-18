import streamlit as st
import libs.utils as utils
import configparser
import os

class App:
    __conf = None
    @staticmethod
    def config():
        if App.__conf is None:  # Read only once, lazy.
            App.__conf = configparser.ConfigParser()
            App.__conf.read('config.ini')
        return App.__conf
    @staticmethod
    def check(path):
        if os.path.isfile("".join([path,"/model.safetensors"])):
            return True
        else: 
            return False
    @staticmethod
    def get(var):
        filepath = App.config().get(section='PATH', option=var, fallback="")
        if filepath !="":
            if os.path.isfile("".join([filepath,"/model.safetensors"])):
                return filepath
            else:
                raise("".join([filepath,"/model.safetensors is not found. (Please fix it in the config.ini)"]))
        else:
            raise("".join(["'",filepath,"' model path is invalid. (Please fix it in the config.ini)"]))
            
    
    
            

if __name__ == '__main__':
    
    
    st.set_page_config(page_title="Main Page",page_icon=":bookmark_tabs:")

    st.title(":blue[A TEXT SUMMARY WEBSITE]")

    # https://docs.streamlit.io/develop/api-reference/widgets
    # st.sidebar.header("Select a demo above")
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    utils.add_logo()



    st.markdown(
        """
        ### Website included:
        - Generate a summary for vietnamese input text and files(WIP).
        - Retrieving recent news from random news outlets with a summary.
        - Spliting laws structure with acts summary 
        - Only supported news and laws citations structure.
    """
    )

    col1, col2 = st.columns(2)
    with col1 :
        st.markdown(
            """
            ### :blue[Project's members info]
            - Student code: 20133030

            - Name: Ngô Hoàng Khánh Duy

            - Github: [Rikun](https://github.com/rqkun)
        """
        )

    with col2:
        st.markdown(
            """
            ### :blue[Project's members info]
            - Student code: 20133066

            - Name: Huỳnh Nhật Minh

            - Github: [MikeDST](https://github.com/MikeDST)
        """
        )

    st.markdown(
        """
        ### Graduation Project of Data Engineering.
        - Project's Counselor: Trần Trọng Bình
    """
    )