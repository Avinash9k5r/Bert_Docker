#########################################################################################################################################################################

import torch
from pytorch_transformers import BertTokenizer
from pytorch_transformers import BertModel
import torch
import numpy as np
import pandas as pd 

#########################################################################################################################################################################

def getDataFromFile():
    import pandas as pd
    df = pd.read_csv('lematized_list.csv')
    lematized_list = df['lematized_list'].tolist()    
    return lematized_list

#########################################################################################################################################################################

def loadBERTModel():

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    return tokenizer , model

#########################################################################################################################################################################

def obtainVectorsforoneword(word , model , tokenizer):                                        
    
    input_ids = torch.tensor(tokenizer.encode(word)).unsqueeze(0) 
    outputs = model(input_ids)
    last_hidden_states = outputs[0]  
    return last_hidden_states

#########################################################################################################################################################################

def getBERTVectors(lematized_list , model , tokenizer):             
    
    cut_lematized_list = lematized_list
    

    a = np.zeros(shape=(2 * len(lematized_list),768)) 
    i = 0   
    j = 0   

    final_list_of_used_words = []

    for idx in range(len(cut_lematized_list)):
        b = obtainVectorsforoneword(cut_lematized_list[idx] , model , tokenizer).detach().numpy()

        if len(b[0]) == 1:
            final_list_of_used_words.append(cut_lematized_list[idx])
            a[i] = b
            i = i + 1

        if len(b[0]) == 2:
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            a[i] = b[0][0]
            i = i + 1
            a[i] = b[0][1]
            i = i + 1
        j = j + 1
        if len(b[0]) != 1 and len(b[0]) != 2:
            continue

    X = a[ : len(final_list_of_used_words)]

    return final_list_of_used_words , X

#########################################################################################################################################################################

def buildDFOfCurrentWordVectorRelation(final_list_of_used_words , X): 
    
    df = pd.DataFrame(X, index=final_list_of_used_words)
    return df

#########################################################################################################################################################################


