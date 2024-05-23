import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import math
import nltk

from bs4 import BeautifulSoup
import pandas as pd
import requests

STOP_PATH='./corpo/vietnamese-stopwords.txt'

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
#ps = PorterStemmer()


def sent_preprocessing(sentences: list) -> list:
    cleaned_sentencs = [sent for sent in sentences if sent]
    for sent in sentences:
        if sent == '' or sent == ' ':
            #print(1)
            continue
    return cleaned_sentencs


def text_preprocessing(sentences: list):
    """
    Pre processing text to remove unnecessary words.
    """
    # print('Preprocessing text')

    stop_words = set()
    with open(STOP_PATH, "r+", encoding="utf-8") as f:
        for line in f:
            stop_words.add(line[:-1])

    clean_words = None
    for sent in sentences:
        words = word_tokenize(sent)
        words = [PorterStemmer.stem(word.lower()) for word in words if word.isalnum()]
        clean_words = [word for word in words if word not in stop_words]

    return clean_words


def create_tf_matrix(sentences: list) -> dict:
    """
    Here document refers to a sentence.
    TF(t) = (Number of times the term t appears in a document) / (Total number of terms in the document)
    """
    # print('Creating tf matrix.')

    tf_matrix = {}

    for sentence in sentences:
        tf_table = {}

        clean_words = text_preprocessing([sentence])
        words_count = len(word_tokenize(sentence))

        # Determining frequency of words in the sentence
        word_freq = {}
        for word in clean_words:
            word_freq[word] = (word_freq[word] + 1) if word in word_freq else 1

        # Calculating relative tf of the words in the sentence
        for word, count in word_freq.items():
            tf_table[word] = count / words_count

        tf_matrix[sentence[:15]] = tf_table

    return tf_matrix


def create_idf_matrix(sentences: list) -> dict:
    """
    Inverse Document Frequency.
    IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
    """
    # print('Creating idf matrix.')

    idf_matrix = {}
    documents_count = len(sentences)
    sentence_word_table = {}

    # Getting words in the sentence
    for sentence in sentences:
        clean_words = text_preprocessing([sentence])
        sentence_word_table[sentence[:15]] = clean_words

    # Determining word count table with the count of sentences which contains the word.
    word_in_docs = {}
    for sent, words in sentence_word_table.items():
        for word in words:
            word_in_docs[word] = (word_in_docs[word] + 1) if word in word_in_docs else 1

    # Determining idf of the words in the sentence.
    for sent, words in sentence_word_table.items():
        idf_table = {}
        for word in words:
            idf_table[word] = math.log10(documents_count / float(word_in_docs[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def create_tf_idf_matrix(tf_matrix, idf_matrix) -> dict:
    """
    Create a tf-idf matrix which is multiplication of tf * idf individual words
    """
    # print('Calculating tf-idf of sentences.')

    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def create_sentence_score_table(tf_idf_matrix) -> dict:
    """
    Determining average score of words of the sentence with its words tf-idf value.
    """
    # print('Creating sentence score table.')

    sentence_value = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0
        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        smoothing = 1
        sentence_value[sent] = (total_score_per_sentence + smoothing) / (count_words_in_sentence + smoothing)

    return sentence_value


def find_average_score(sentence_value):
    """
    Calculate average value of a sentence form the sentence score table.
    """
    # print('Finding average score')


    sum = 0
    for val in sentence_value:
        sum += sentence_value[val]

    average = sum / len(sentence_value)

    return average


def generate_summary(sentences, sentence_value, max_char):
    """
    Generate a sentence for sentence score greater than average.
    """
    # print('Generating summary')

    sentence_count = 0
    char_count = 0
    chosen_sent = []
    summary = ''

    sorted_sentence_value = sorted(sentence_value.items(), reverse= True, key=lambda kv: (kv[1], kv[0]))

    # convert to dict
    sorted_sentence_value_dict = {}
    for sent, score in sorted_sentence_value:
        sorted_sentence_value_dict.setdefault(sent, []).append(score)

    # print('sorted_sentence_value_dict: ', sorted_sentence_value_dict)

    for sent, score in sorted_sentence_value_dict.items():
        found_sent = next((x for x in sentences if sent == x[:15]), None)
        char_count += len(found_sent)
        if char_count > max_char: break
        else : chosen_sent.append(sent)

    for sentence in sentences:
        if sentence[:15] in chosen_sent:
            summary += sentence + " "
            sentence_count += 1

    return summary

def TF_IDF(text, max_char):
    sentences = sent_tokenize(text)
    # print('Sentences', sentences)

    # sentences = sent_preprocessing(sentences)

    tf_matrix = create_tf_matrix(sentences)
    # print('TF matrix', tf_matrix)

    idf_matrix = create_idf_matrix(sentences)
    # print('IDF matrix',idf_matrix)

    tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)
    # print('TF-IDF matrix', tf_idf_matrix)
    # print('First document tfidf',tf_idf_matrix[list(tf_idf_matrix.keys())[0]])

    sentence_value = create_sentence_score_table(tf_idf_matrix)
    # print('Sentence Scores', sentence_value)

    # threshold = find_average_score(sentence_value)
    # print('Threshold', threshold)

    return(generate_summary(sentences, sentence_value, max_char))

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


    danviet_df = pd.DataFrame(columns=["title", "abstract", "content", "image_url"])

    for item in danviet_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"class":"entry-body dtdefault clearfix", "data-role":"content"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            content = content + text.get_text() + " "
        danviet_df = danviet_df._append({"title":item["title"], "abstract":item["description"], "content":content, "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)


    tuoitre_df = pd.DataFrame(columns=["title", "abstract", "content", "image_url"])

    for item in tuoitre_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"class":"detail-content afcbc-body", "data-role":"content"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            content = content + text.get_text() + " "
        tuoitre_df = tuoitre_df._append({"title":item["title"], "abstract":item["description"], "content":content, "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    laodong_df = pd.DataFrame(columns=["title", "abstract", "content", "image_url"])

    for item in laodong_API_Data:
        if item["image_url"] == None: continue
        page = requests.get(item["link"], verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        content_body = soup.find("div", attrs={"id":"gallery-ctt", "class":"art-body"})
        if content_body == None: continue
        content = ""
        for text in content_body.find_all("p"):
            content = content + text.get_text() + " "
        laodong_df = laodong_df._append({"title":item["title"], "abstract":item["description"], "content":content, "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    vnexpress_df = pd.DataFrame(columns=["title", "abstract", "content", "image_url"])

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
            content = content + small_content_text + " "
        vnexpress_df = vnexpress_df._append({"title":item["title"], "abstract":item["description"], "content":content, "image_url":(item["image_url"]).replace(".webp", "")}, ignore_index=True)

    frames = [danviet_df.head(4), tuoitre_df.head(4), laodong_df.head(4), vnexpress_df.head(4)]
    latest_new_df = pd.concat(frames)
    latest_new_df.reset_index(inplace=True, drop=True)
    return(latest_new_df)


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