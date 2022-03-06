#############################################################################################################################################################################

import pandas as pd
from sklearn.cluster import KMeans 
import sys
from kneed import KneeLocator

#########################################################################################################################################################################

def getDataFromFile():

    
    df = pd.read_csv('final_list_of_used_words.csv')
    final_list_of_used_words = df['final_list_of_used_words'].tolist()     

    df = pd.read_csv('X.csv')
    X = df

    return final_list_of_used_words , X

#########################################################################################################################################################################
# WE DO THE ELBOW ETHOD HERE 

def printElbowMethodGraph(X):

    
    range_of_ssc = 12

    cost =[]
    for i in range(1, range_of_ssc):
        KM = KMeans(n_clusters = i, max_iter = 500)
        KM.fit(X)

        # calculates squared error
        # for the clustered points
        cost.append(KM.inertia_)     
    
    
    sys.path.append('..')

    
    kn = KneeLocator(list(range(1, range_of_ssc)), cost, S=1.0, curve='convex', direction='decreasing')

    return kn.knee
    # the point of the elbow is the 
    # most optimal value for choosing k

#########################################################################################################################################################################

def writeToFile(knee_point_value):

    file = open('knee_point_value.txt' , "w")
    file.write(str(knee_point_value))
    file.close()
    
#########################################################################################################################################################################




