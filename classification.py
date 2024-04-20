import re
import requests
import streamlit as st
from nltk.tokenize import sent_tokenize
from label_config import multicalss_labels, binary_labels
from api_config import MULTICLASS_API_URL, BINARY_API_URL, API_TOKEN

import nltk
nltk.download('punkt')


def multiclass_threshold_classification(sentences, threshold=0.5):
    
    # processing sentences for multiclass classification with threshold
    api_result = requests.post(MULTICLASS_API_URL,
                               headers={"Authorization": f"Bearer {API_TOKEN}"},
                               json={"inputs": [sentence['sentence']
                                                for sentence in sentences]}).json()
    
    if isinstance(api_result, dict) and api_result.get('error'):
        st.error(api_result['error'])
        print(api_result['error'])
        return "No multiclass label found"
    else:
        for sen_lst, api_lst in zip(sentences, api_result):
            if api_lst[0]['score'] >= threshold:
                sen_lst['label'] = multicalss_labels[int(api_lst[0]['label'].split('_')[1])]
                sen_lst['confidence'] = api_lst[0]['score']
            else:
                sen_lst['label'] = binary_labels[0]
                sen_lst['confidence'] = None
    return sentences
    

def multiclass_classification(sentences):
    
    # processing sentences with unfair binary labels for multiclass classification
    api_result = requests.post(MULTICLASS_API_URL,
                               headers={"Authorization": f"Bearer {API_TOKEN}"},
                               json={"inputs": [sentence['sentence']
                                                for sentence in sentences
                                                if sentence['binary_label'] == 'Unfair']}).json()
    
    if isinstance(api_result, dict) and api_result.get('error'):
        st.error(api_result['error'])
        print(api_result['error'])
        return "No multiclass label found"
    else:
        for i, lst in enumerate(api_result):
            sentences[i]['multiclass_label'] = multicalss_labels[int(lst[0]['label'].split('_')[1])]
    return sentences


def binary_classification(sentences):
    
    # sorting sentences by binary classification(unfair, fair)
    api_result = requests.post(BINARY_API_URL,
                               headers={"Authorization": f"Bearer {API_TOKEN}"},
                               json={"inputs": [sentence['sentence']
                                                for sentence in sentences]}).json()
    
    if isinstance(api_result, dict) and api_result.get('error'):
        st.error(api_result['error'])
        print(api_result['error'])
        return "No binary label found"
    else:
        for i, lst in enumerate(api_result):
            sentences[i]['binary_label'] = binary_labels[int(lst[0]['label'].split('_')[1])]
    return sentences


def process_text(text):
    
    # splitting text into a list of sentences and cleaning the text
    # creating a dictionary of sentences, attributes are binary_label and multiclass_label
    cleaned_text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\x0c', ' ')
    sentences = sent_tokenize(cleaned_text)
    
    sentences = [{"sentence": sentence, "label": None, "confidence": None}
                 for sentence in sentences if len(sentence.split()) > 5]
    
    # classification
    sentences = multiclass_threshold_classification(sentences)
    return sentences

