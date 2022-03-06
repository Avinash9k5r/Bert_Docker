##########################################################################################################################################################################

import pandas as pd
import nltk
import spacy 
nlp = spacy.load('en_core_web_sm')
nltk.download('tagsets')  

#########################################################################################################################################################################

def convertFileToVar():
    
    df = pd.read_csv('lematized_list.csv')
    lematized_list = df['lematized_list'].tolist()     
    file = open('text_cpy_ner_spacy.txt', 'r')
    text_copy_for_ner_spacy = file.read()               
    file.close()
    return lematized_list , text_copy_for_ner_spacy

#########################################################################################################################################################################

def POSbyNLTK(lematized_list):                  
    
    print(len(lematized_list)) 
    lematized_string = ' '.join([str(elem) for elem in lematized_list]) 

    def preprocess(sent):
        sent = nltk.word_tokenize(sent)
        sent = nltk.pos_tag(sent)
        return sent

    sent = preprocess(lematized_string) 
    return sent

#########################################################################################################################################################################

def POSBySpacy(text_copy_for_ner_spacy):          

    
    sentence = text_copy_for_ner_spacy
    doc = nlp(sentence)

    ner_spacy_tokens_list = []

    for token in doc:
        ner_spacy_tokens_list.append([token.text , token.pos_])

    for word in ner_spacy_tokens_list: 
        word[0] = word[0].lower()

    return ner_spacy_tokens_list

#########################################################################################################################################################################

def getAllNounsFromText(sent , ner_spacy_tokens_list):   
                               
    list_noun_words = []

    for i in sent:
        if i[1] == 'NN' or i[1] == 'NNP' or i[1] == 'NNPS' or i[1] == 'NNS':
            list_noun_words.append(i[0])

    for i in ner_spacy_tokens_list:
        if i[1] == 'NOUN' or i[1] == 'PROPN':
            list_noun_words.append(i[0])

    for idx in range(len(list_noun_words)):
        temp = list_noun_words[idx].lower()

    list_noun_words = list(set(list_noun_words))

    return list_noun_words

#########################################################################################################################################################################

def printPOSOfAWordFromText(ner_spacy_tokens_list , sent , word_name):

    for word in sent:
        if word[0] == word_name:
            print(word[1] , "BY NLTK")

    for word in ner_spacy_tokens_list:
        if word[0] == word_name:
            print(word[1] , "BY Spacy")     
            

#########################################################################################################################################################################

def writetoOutput(list_noun_words):

    df= pd.DataFrame(list_noun_words , columns=["list_noun_words"])
    df.to_csv('list_noun_words.csv' , index = False)

#########################################################################################################################################################################




