import os
print(os.getcwd())
from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)

import nltk 
from nltk.corpus import stopwords
import re
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
#!pip install pytorch_transformers
import torch
from pytorch_transformers import BertTokenizer
from pytorch_transformers import BertModel
from nltk.stem import WordNetLemmatizer # LEMMATIZATION OVER FILTERED_WORDS

import logging
logging.basicConfig(filename='BERT-API_called_from_rasa.log', level=logging.DEBUG , format='%(asctime)s :: %(levelname)s :: %(message)s', force=True)
#################################################################################################################
from flask import request
from main_search_api import searchFunc
from get_arango_query_for_search_string import get_query_from_db
from get_arango_query_for_search_string import get_list_of_filenames_of_urls
##################################################################
# Since we need the csv file containing all the vectors of all the keywords across all files, we download it from s3 now.

# need to be in the right folder
import os
curr_path = os.getcwd()
#os.chdir("../")
src_path = os.getcwd()
new_path = os.path.join(src_path ,'output')
print(new_path)
os.chdir(new_path)
print(os.getcwd())

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    import boto3
    import os
    from dotenv import load_dotenv
    load_dotenv()
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    s3_resource = boto3.resource('s3',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key= aws_secret_access_key)
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path
from dotenv import load_dotenv
load_dotenv()
bucketname = os.getenv('bucketname')
downloadDirectoryFroms3(bucketname , "all_keyword_vectors") 

os.chdir(curr_path)
print(os.getcwd())
##################################################################
from one_time_load_files import one_load_files
lemmatizer , stop_words = one_load_files()
##################################################################
word_map_dictionary = get_query_from_db()
list_of_filenames_generated = get_list_of_filenames_of_urls()
##################################################################
class TodoSimple(Resource):
    def get(self):
        inputstr = request.form['text']
        print(inputstr)
        logging.info("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        logging.info("The keyword obtained by BERT-API is " + inputstr)
        retval , retval1 = searchFunc(word_map_dictionary , inputstr , lemmatizer , stop_words , list_of_filenames_generated)
        retdict = []
        for idx in range(len(retval)):
            retdict.append([retval[idx] , retval1[idx]])
        
        print("))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))")
        print(retdict[0])
        
        logging.info("The article-URL returned by BERT-API for keyword " + inputstr + " is : " + str(retval[0][0]))
        
        return {'para': retval1[0] , 'url': retval[0]}

################################################################################################################

################################################################################################################
#####################################

stop_words = stopwords.words('english') #do-1
stop_words.extend(['us','etc','god','jesus','lord','evil','devil','man','israel','people','son','men','house','day','children','land','things','hand','earth','sons','son','jerusalem','city','father' , 'what' , 'does' , 'bible' , 'say' , 'about' , 'on' , 'christianity'])

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

lemmatizer = WordNetLemmatizer()

from sklearn.metrics import pairwise_distances_argmin_min
######################################
def sentence_vec(var , stop_words , tokenizer , model , lemmatizer):

    
    text = re.sub(r'[^a-zA-Z]',' ',var) #no-2
    text = re.sub(r'\s+',' ',text)
    text = text.lower()
    text = re.sub(r'\d',' ',text)


    sentences = nltk.sent_tokenize(text) #no-3
    sentences = [nltk.word_tokenize(sentence) for sentence in sentences]


    # for i in range(len(sentences)): #no-4
    #     sentences[i] = [word for word in sentences[i] if word not in stop_words]

    print(sentences)  
    filtered_sentence = sentences





    lematized_list = []
    for word in filtered_sentence[0]:
        lematized_list.append(lemmatizer.lemmatize(word ,  pos="v"))
    lematized_list_short = list(set(lematized_list))
    lematized_list_short = lematized_list ### wasnt here before. added here on monday morning.

    print(len(lematized_list))

    print(len(lematized_list_short))


    

    def obtainVectors(word):

        input_ids = torch.tensor(tokenizer.encode(word)).unsqueeze(0)  # Batch size 1
        outputs = model(input_ids)
        last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple
        return last_hidden_states





    import numpy as np
    a = np.zeros(shape=(5 * len(lematized_list_short),768)) #####
    i = 0   # i marks row-no
    j = 0   # j marks iteration-no
    print(a)

    final_list_of_used_words = []
    cut_lematized_list = lematized_list_short 

    for idx in range(len(cut_lematized_list)):
        b = obtainVectors(cut_lematized_list[idx]).detach().numpy()
        print(len(b[0]) , j)

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
            
        if len(b[0]) == 3:                                                  # 3 here
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            a[i] = b[0][0]
            i = i + 1
            a[i] = b[0][1]
            i = i + 1
            a[i] = b[0][2]
            i = i + 1    

        if len(b[0]) == 4:                                                   #4 here
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            a[i] = b[0][0]
            i = i + 1
            a[i] = b[0][1]
            i = i + 1
            a[i] = b[0][2]
            i = i + 1    
            a[i] = b[0][3]
            i = i + 1    
        
        
        if len(b[0]) == 5:                                                   #5 here
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            final_list_of_used_words.append(cut_lematized_list[idx])
            a[i] = b[0][0]
            i = i + 1  
            a[i] = b[0][1]
            i = i + 1
            a[i] = b[0][2]
            i = i + 1    
            a[i] = b[0][3]
            i = i + 1    
            a[i] = b[0][4]
            i = i + 1    
        
        
        j = j + 1

        if len(b[0]) != 1 and len(b[0]) != 2:
            continue



    print(type(a))
    print(a)
    X = a[ : len(final_list_of_used_words)]
    print(X)
    print(len(X))        


    
    return X , final_list_of_used_words

######################################
import os
curr_path = os.getcwd()
#os.chdir('../')
src_dir =  os.getcwd()
new_path = os.path.join(src_dir ,'output')
new_path = os.path.join(new_path , 'all_keyword_vectors')
os.chdir(new_path)
import pandas as pd
file = pd.read_csv("all_keywords_vectors.csv")
os.chdir(curr_path)
print(os.getcwd())
df = pd.DataFrame(file)
list_of_words_final = df['word'].tolist()
df.drop(['word' , 'Unnamed: 0'], inplace = True,  axis = 1) 
A = df.to_numpy() 
print(type(df))
print(type(A))
Y = A
######################################

######################################
def func(Y , list_of_words_final ,  inputstr):  # this func will calculate the bert substitute keyword for the mismatched word, from our list of words.
   # try:
    X , words_in_sentence = sentence_vec(inputstr , stop_words , tokenizer , model , lemmatizer)
    print(X)
    print(words_in_sentence)

    closest, dist = pairwise_distances_argmin_min(X, Y , metric='euclidean')
    print(len(closest))
    print("idx -> " , closest)

    for i in range(len(words_in_sentence)):
        print('word found from final_list_of_used_word == ' , words_in_sentence[i] , ' -> ' , list_of_words_final[closest[i]] , "    dist -> " , dist[i])
        key_word = list_of_words_final[closest[i]]
    return {'keyword': key_word}
    #except:
     #   return {'keyword': ""}
################################################################################################################
class changeKeyword(Resource):
    def get(self):
        inputstr = request.form['text']
        print(inputstr)
        logging.info("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        logging.info("The mismatched-keyword obtained by BERT-API is " + inputstr)

        matched_kw = func(Y , list_of_words_final , inputstr) # (Y , list_of_words_final) -> these are global in this file.
        # return list of newly matched keyword here.
      
        logging.info("The keyword, matched from list of avilable keywords as returned by BERT-API for " + inputstr + " is : " + str(matched_kw))
        return matched_kw

###############################################################################################################------------------------------------------------------------------------------------------------------------------------------





print(os.getcwd())

api.add_resource(TodoSimple, '/str')
api.add_resource(changeKeyword, '/kw')



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8002 , debug=True)
