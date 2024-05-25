import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import math
import nltk

from string import ascii_lowercase

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

def remove_unnecessary(input: str):

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

def sent_preprocessing(sentences: list) -> list:
    cleaned_sentencs = [sent for sent in sentences if sent]
    for sent in sentences:
        if sent == '' or sent == ' ':
            #print(1)
            continue
    return cleaned_sentencs

def dieu_tokenize(luat) -> list:
    Dieu_List = []
    D_found = []
    for dieu in range(1, 65):
        sub_str = "Điều " + str(dieu) + "."
        D_found.append(luat.find(sub_str))

    for j in range(0, len(D_found)):
        if D_found[j] == -1:
            continue
        elif j == 63 or D_found[j+1] == -1:
                Dieu_List.append(luat[D_found[j]:])
                continue
        Dieu_List.append(luat[D_found[j]:D_found[j+1]])
    return Dieu_List

def text_preprocessing_list(sentences: list):

    # Pre processing text to remove unnecessary words.

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

def text_preprocessing(sentence):
    """
    Pre processing text to remove unnecessary words.
    """
    # print('Preprocessing text')

    stop_words = set()
    with open('vietnamese-stopwords.txt', "r+", encoding="utf-8") as f:
        for line in f:
            stop_words.add(line[:-1])

    clean_words = None
    words = word_tokenize(sentence)
    words = [PorterStemmer.stem(word.lower()) for word in words if word.isalnum()]
    clean_words = [word for word in words if word not in stop_words]

    return clean_words


def create_tf_matrix(sentence) -> dict:
    """
    Here document refers to a sentence.
    TF(t) = (Number of times the term t appears in a document) / (Total number of terms in the document)
    """
    # print('Creating tf matrix.')
    if sentence[0] == " ": sentence = sentence[1:]
    if sentence[len(sentence)-1] == " ": sentence = sentence[:len(sentence)-1]
    tf_matrix = {}

    # for sentence in sentences:
    tf_table = {}

    clean_words = text_preprocessing(sentence)
    #print(clean_words)
    words_count = len(word_tokenize(sentence))

    # Determining frequency of words in the sentence
    word_freq = {}
    for word in clean_words:
        word_freq[word] = (word_freq[word] + 1) if word in word_freq else 1

    # Calculating relative tf of the words in the sentence
    for word, count in word_freq.items():
        tf_table[word] = count / words_count

    # tf_matrix[sentence[:15]] = tf_table
    tf_matrix[sentence] = tf_table

    return tf_matrix


def create_idf_matrix(sentences: list) -> dict:
    """
    Inverse Document Frequency.
    IDF(t) = log_10(Total number of documents / Number of documents with term t in it)
    """
    # print('Creating idf matrix.')
    idf_matrix = {}
    documents_count = len(sentences)
    sentence_word_table = {}

    # Getting words in the sentence
    for sentence in sentences:
        if sentence[0] == " ": sentence = sentence[1:]
        if sentence[len(sentence)-1] == " ": sentence = sentence[:len(sentence)-1]

        clean_words = text_preprocessing(sentence)
        print(sentence)
        # sentence_word_table[sentence[:15]] = clean_words
        sentence_word_table[sentence] = clean_words

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

    tf_idf_matrix = {}

    for sent2, f_table2 in idf_matrix.items():
        sent1 = list(tf_matrix.keys())[0]
        f_table1 = list(tf_matrix.values())[0]
        print("'"+sent1+"'")
        print("'"+sent2+"'")
        if sent1 == sent2:
            print("Equal")
            tf_idf_table = {}
            for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):
                tf_idf_table[word1] = float(value1 * value2)
            tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def create_sentence_score_table(dieu, tf_idf_matrix) -> dict:
    """
    Determining average score of words of the sentence with its words tf-idf value.
    """

    sentences = sent_tokenize(dieu)

    sentence_value = {}

    for sentence in sentences:
        words = word_tokenize(sentence)
    
        for sent, f_table in tf_idf_matrix.items():
            total_score_per_sentence = 0
            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                if word in words:
                    total_score_per_sentence += score

            smoothing = 1
            sentence_value[sentence] = (total_score_per_sentence + smoothing) / (count_words_in_sentence + smoothing)

    return sentence_value


def find_average_score(sentence_value):
    """
    Calculate average value of a sentence form the sentence score table.
    """
    sum = 0
    for val in sentence_value:
        sum += sentence_value[val]

    average = sum / len(sentence_value)

    return average


def generate_summary(dieu, sentence_value, max_char):
    """
    Generate a sentence for sentence score greater than average.
    """
    # print('Generating summary')
    sentences = sent_tokenize(dieu)
    sentence_count = 0
    char_count = 0
    chosen_sent = []
    summary = ''

    sorted_sentence_value = sorted(sentence_value.items(), reverse= True, key=lambda kv: (kv[1], kv[0]))

    # convert to dict
    sorted_sentence_value_dict = {}
    for sent, score in sorted_sentence_value:
        sorted_sentence_value_dict.setdefault(sent, []).append(score)

    for sent, score in sorted_sentence_value_dict.items():
        found_sent = next((x for x in sentences if sent == x), None)
        char_count += len(found_sent)
        if char_count > max_char: break
        else : chosen_sent.append(sent)

    for sentence in sentences:
        if sentence in chosen_sent:
            summary += sentence + " "
            sentence_count += 1

    return summary

def TF_IDF(luat, dieu, max_char):
    dieu = add_dot(dieu)
    luat = add_dot(luat)

    dieu = dieu.replace("\n", " ")
    luat = luat.replace("\n", " ")

    dieu = remove_unnecessary(dieu)
    luat = remove_unnecessary(luat)

    dieues = dieu_tokenize(luat)

    tf_matrix = create_tf_matrix(dieu)
    idf_matrix = create_idf_matrix(dieues)
    tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)
    sentence_value = create_sentence_score_table(dieu, tf_idf_matrix)

    return(generate_summary(dieu, sentence_value, max_char))