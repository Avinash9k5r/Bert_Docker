###########################################################################################################################################################

import nltk 
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer 
nltk.download('wordnet')
import pandas as pd

###########################################################################################################################################################

def listOfNamesOfUrl(url_list):  # ret-type -> [ [url , name] , [url , name] , [url , name]  .... ]
    url_and_name_list = []
    for url in url_list:
        import re                                       
        filteredurl = re.sub(r'[^a-zA-Z]',' ',url)
        filteredurl = re.sub(r' ' , '_',filteredurl)
        filename =  "_" + filteredurl + ".txt"
        url_and_name_list.append([url , filename])
    return url_and_name_list
##################################################################################################################################################################

def convertFileToVar(article_filename):

    file = open(article_filename)                                                                    
    var = file.read()                                                                                  
    file.close()
    return var

##################################################################################################################################################################

def removespecialchars(var):                                              
    import re
    text = re.sub(r'[^a-zA-Z]',' ',var) 
    text = re.sub(r'\s+',' ',text)
    text = text.lower()
    text = re.sub(r'\d',' ',text)
    
    text_copy_for_ner_spacy = text + ' '
    return text , text_copy_for_ner_spacy

##################################################################################################################################################################

def tokenizeAndRemoveStopwords(text):               
    

    stop_words = stopwords.words('english') 
    stop_words.extend(['us','etc','god','jesus','lord','evil','devil','man','israel','people','king','son','men','house','day','children','land','things','hand','earth','sons','son','jerusalem','city','father','bible','tlb'])

    sentences = nltk.sent_tokenize(text) 
    sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    for i in range(len(sentences)): 
        sentences[i] = [word for word in sentences[i] if word not in stop_words]

    filtered_sentence = sentences
    return filtered_sentence

#################################################################################################################################################################

def lemmatize(filtered_sentence):

    lemmatizer = WordNetLemmatizer()

    lematized_list = []
    for word in filtered_sentence[0]:
        lematized_list.append(lemmatizer.lemmatize(word ,  pos="v"))
    lematized_list_short = list(set(lematized_list))
    lematized_list_short = lematized_list


    print(len(lematized_list))
    print(len(lematized_list_short))
    return lematized_list

################################################################################################################################################################

def writeToFile(lematized_list , text_copy_for_ner_spacy):

    df = pd.DataFrame(lematized_list , columns=['lematized_list'])
    df.to_csv('lematized_list.csv' , index = False)

    file = open('text_cpy_ner_spacy.txt' , "w")
    file.write(text_copy_for_ner_spacy)
    file.close()

################################################################################################################################################################


