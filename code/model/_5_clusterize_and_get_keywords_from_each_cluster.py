#########################################################################################################################################################################

import pandas as pd
from sklearn.cluster import KMeans
import numpy as np     
import numpy as np
import pandas as pd

#########################################################################################################################################################################

def getDataFromFile():

    
    df = pd.read_csv('final_list_of_used_words.csv')
    final_list_of_used_words = df['final_list_of_used_words'].tolist()     

    df = pd.read_csv('X.csv')               
    X = df.to_numpy()

    file = open('knee_point_value.txt', 'r')
    knee_point_value = file.read()                                         
    file.close()
    knee_point_value = int(knee_point_value)

    df = pd.read_csv('list_noun_words.csv')
    list_noun_words = df['list_noun_words'].tolist()                        

    df = pd.read_csv('lematized_list.csv')
    lematized_list = df['lematized_list'].tolist()     

    output_filename = 'top_noun_words_from_each_cluster.txt'
    
    return final_list_of_used_words , X , knee_point_value , list_noun_words , lematized_list , output_filename

#########################################################################################################################################################################

def makeKClusters(num_of_clusters , X):
    
    km = KMeans(n_clusters = num_of_clusters)
    y = km.fit_predict(X) 
    km.cluster_centers_[0]  
    return km , y

#########################################################################################################################################################################

def removeAllWordsExceptNounsFromDF(final_list_of_used_words , X , list_noun_words):
                                                                               
    remove_these_indices = []
    for idx in range(len(final_list_of_used_words)):
        final_list_of_used_words[idx] = str(final_list_of_used_words[idx])
        if final_list_of_used_words[idx] not in list_noun_words:
            remove_these_indices.append(idx)

    for word in reversed(remove_these_indices): 
        del final_list_of_used_words[word]
        X = np.delete(X,word, 0)

    return final_list_of_used_words , X

#########################################################################################################################################################################

def getTopNounsFromEachCluster(km , final_list_of_used_words , X , lematized_list_cpy , num_of_clusters):     
    
    list_all_words = []
    for word in lematized_list_cpy:
        list_all_words.append(word)
    from sklearn.metrics import pairwise_distances_argmin_min  
    
    words_by_cluster_no = [[] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , [] , []] 
    
    total_iterations = min((100 / num_of_clusters) , ((len(final_list_of_used_words) / num_of_clusters) -1)) 
    
    str_to_store_cluster_idx_and_distance = ""

        
    j = 1
    closest_overall_output_words = []
    while(j <= total_iterations):
        closest_single_itr, distance_closest_single_itr = pairwise_distances_argmin_min(km.cluster_centers_, X ,metric='euclidean')
        t = 1

        for i in range(len(closest_single_itr)):
            words_by_cluster_no[t].append([final_list_of_used_words[closest_single_itr[i]],distance_closest_single_itr[i]])
            t += 1
            closest_overall_output_words.append(final_list_of_used_words[closest_single_itr[i]])

        
        for i in range(len(closest_single_itr)): 
            final_list_of_used_words[closest_single_itr[i]] = 0 
        
        
        for word in final_list_of_used_words: 
            if word == 0:
                final_list_of_used_words.remove(word)

        X = np.delete(X, closest_single_itr, 0) 
        

        print("this is j here :",j)
        j = j + 1

    return closest_overall_output_words , words_by_cluster_no , final_list_of_used_words , X , list_all_words

#########################################################################################################################################################################

def save_cluster_keywords_to_file(words_by_cluster_no , output_filename_clusters , knee_point_value):
    i = 0
    
    file = open(output_filename_clusters , 'w')
    file.write("")
    file.close()
    
    file = open(output_filename_clusters , 'a')
    
    while(i < knee_point_value):
        val = "cluster no : " + str(i+1) + " : "
        file.write(val)
        val = ""
        for word in words_by_cluster_no[i]:
            val = val + str(word) + "    "
        val = val + '\n\n'    
        file.write(val)        
        print(val + "  ->  ")
        i += 1
        
    file.close()
        
#########################################################################################################################################################################

def mergeNounsFromEachCluster(words_by_cluster_no , list_all_words): 

    final_1st_lvl_out_listof_words = []
    words_by_cluster_no_set = []
    words_by_cluster_no_set_with_distances = []
    words_by_cluster_no_set_with_distances_and_frequency = []#
    for array_idx in range(len(words_by_cluster_no)):
        temp_list_mapped = []
        temp_list = []
        if len(words_by_cluster_no[array_idx]) == 0:
            continue
        
        for word_mapping in words_by_cluster_no[array_idx]:
            if (word_mapping[0] not in temp_list) and (len(temp_list)<5):
                freq = frequencyOfWordInText(word_mapping[0] , list_all_words)#
                word_mapping.append(freq)#
                temp_list.append(word_mapping[0])
                temp_list_mapped.append(word_mapping)
                final_1st_lvl_out_listof_words.append(word_mapping[0])
        
        words_by_cluster_no_set.append(temp_list)
        words_by_cluster_no_set_with_distances.append(temp_list_mapped)



    return final_1st_lvl_out_listof_words , words_by_cluster_no_set , words_by_cluster_no_set_with_distances

#########################################################################################################################################################################

def frequencyOfWordInText(word_to_find , list_of_all_words):
    
    count = 0
    for word in list_of_all_words:
        if word == word_to_find:
            count += 1
                             
    return count            

#########################################################################################################################################################################

def listToString(s): # Python program to convert a list to string
    
    str1 = "" 
    for i in range(len(s)):
        str1 = str(str1) + str(s[i]) + " ; "
        
    str1 = str1[0:-2] + '.'
    return str1

#########################################################################################################################################################################

def writeTo1stLvlOutput(output_filename , out_words_list_for_mapping , lematized_list):
    
    
    df = pd.DataFrame(out_words_list_for_mapping , columns=['out_words_list_for_mapping'])
    df.to_csv(output_filename , index = False)

#########################################################################################################################################################################

