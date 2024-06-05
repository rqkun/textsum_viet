import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import math
import nltk

from bs4 import BeautifulSoup
import pandas as pd
import requests
from string import ascii_lowercase

from libs import TFIDF_law
from libs import TFIDF_news

STOP_PATH='./corpo/vietnamese-stopwords.txt'

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def add_dot(input):
    EndLine = (input.replace('\n', '™'))

    EndLinePos = EndLine.find('™')
    while EndLinePos != -1:
        if EndLine[EndLinePos-1] == ".":
            EndLine = EndLine[:EndLinePos] + "\n" + EndLine[EndLinePos+1:]
        elif EndLine[EndLinePos-1] == ":" or EndLine[EndLinePos-1] == ";" or EndLine[EndLinePos-1] == ",":
            EndLine = EndLine[:EndLinePos-1] + ".\n" + EndLine[EndLinePos+1:]
        else:
            EndLine = EndLine[:EndLinePos] + ".\n" + EndLine[EndLinePos+1:]
        EndLinePos = EndLine.find('™')
    return(EndLine)

def remove_unnecessary(input):

    for dieu in range(1, 100):
        sub_str = "Điều " + str(dieu) + "."
        new_sub_str = "Điều " + str(dieu) + "_"
        input = input.replace(sub_str, new_sub_str)

    for num in range(1, 100):
        sub_str = str(num) + ". "
        input = input.replace(sub_str, "")

    for char in ascii_lowercase:
        sub_str = str(char) + ") "
        input = input.replace(sub_str, "")
    
    input = input.replace("_", ".")
    return input

def TF_IDF_laws(luat, dieu, max_char):
    return TFIDF_law.TF_IDF(luat, dieu, max_char)

def TF_IDF_news(text, max_char):
    return TFIDF_news.TF_IDF(text, max_char)

def create_Dict(input) -> dict:
    Dieu_dict = {}
    D_found = []
    for dieu in range(1, 100):
        sub_str = "Điều " + str(dieu) + "."
        D_found.append(input.find(sub_str))

    for j in range(0, len(D_found)):
        if D_found[j] == -1:
            continue
        elif D_found[j] != -1 and D_found[j+1] == -1:
                #Dieu_List.append(input[D_found[j]:])
                content = input[D_found[j]:]
                EndLine = (content.replace('\n', '™')).find('™')
                Dieu_dict[content[:EndLine]] = content[EndLine+1:]
                continue
        #Dieu_List.append(input[D_found[j]:D_found[j+1]])
        content = input[D_found[j]:D_found[j+1]]
        EndLine = (content.replace('\n', '™')).find('™')
        Dieu_dict[content[:EndLine]] = content[EndLine+1:]

    return Dieu_dict

def get_latest_news():
    response = requests.get('https://newsdata.io/api/1/latest?country=vi&domain=danviet&apikey=pub_444565f16afae854bd6a1d0205b18e494686f')
    API_Data = response.json() 
    danviet_API_Data = API_Data["results"]


    response = requests.get('https://newsdata.io/api/1/latest?country=vi&domain=tuoitre&apikey=pub_444565f16afae854bd6a1d0205b18e494686f')
    API_Data = response.json()
    tuoitre_API_Data = API_Data["results"]


    response = requests.get('https://newsdata.io/api/1/latest?country=vi&domain=laodong_vn&apikey=pub_444565f16afae854bd6a1d0205b18e494686f')
    API_Data = response.json()
    laodong_API_Data = API_Data["results"]


    response = requests.get('https://newsdata.io/api/1/latest?country=vi&domain=vnexpress&apikey=pub_444565f16afae854bd6a1d0205b18e494686f')
    API_Data = response.json()
    vnexpress_API_Data = API_Data["results"]


    danviet_df = pd.DataFrame(columns=["title", "abstract", "content", "link", "image_url"])

    for item in danviet_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"class":"entry-body dtdefault clearfix", "data-role":"content"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            if text.get_text() not in content:
                content = content + text.get_text() + " "
        danviet_df = danviet_df._append({"title":item["title"], "abstract":item["description"], "content":content, "link":item["link"], "image_url":(item["image_url"]).replace(".webp", "")},  ignore_index=True)


    tuoitre_df = pd.DataFrame(columns=["title", "abstract", "content", "link", "image_url"])

    for item in tuoitre_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"class":"detail-content afcbc-body", "data-role":"content"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            if text.get_text() not in content:
                content = content + text.get_text() + " "
        tuoitre_df = tuoitre_df._append({"title":item["title"], "abstract":item["description"], "content":content,"link":item["link"], "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    laodong_df = pd.DataFrame(columns=["title", "abstract", "content", "link", "image_url"])

    for item in laodong_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"id":"gallery-ctt", "class":"art-body"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            if text.get_text() not in content:
                content = content + text.get_text() + " "
        laodong_df = laodong_df._append({"title":item["title"], "abstract":item["description"], "content":content,"link":item["link"], "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    vnexpress_df = pd.DataFrame(columns=["title", "abstract", "content", "link", "image_url"])

    for item in vnexpress_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content = ""
        for small_content in soup.find_all("p", attrs={"class":"Normal"}):
            if small_content.get('style') != None:
                if small_content['style'] == "text-align:right;":
                    continue
            if small_content.get('align') != None:
                if small_content['align'] == "right":
                    continue
            small_content_text = small_content.get_text()
            if small_content == None: 
                break
            if "Video: " in small_content_text:
                break
            if text.get_text() not in content:
                content = content + small_content_text + " "
        vnexpress_df = vnexpress_df._append({"title":item["title"], "abstract":item["description"], "content":content,"link":item["link"], "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    frames = [danviet_df.head(4), tuoitre_df.head(4), laodong_df.head(4), vnexpress_df.head(4)]
    latest_new_df = pd.concat(frames)
    latest_new_df.reset_index(inplace=True, drop=True)
    return(latest_new_df)

def get_law_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    content = ""
    for line in soup.find_all("p"):
        content += line.get_text()[:len(line.get_text())]
    
    content = content.replace("\t", "")

    content = add_dot(content)
    content = remove_unnecessary(content)

    return content

def is_url(url):
    if "https://" not in url: return False
    return True

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/pt3bm6M.png/200/200);
                background-repeat: no-repeat;
                background-size: 200px;
                padding-top: 120px;
                background-position: 60px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: " ";
                margin-left: 60px;
                margin-top: 20px;
                font-size: 40px;
                position: relative;
                top: 60px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )