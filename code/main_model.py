#########################################################################################
# IF YOU ARE RUNNING THIS FILE WITHOUT DOCKER, COMMENT THESE 4 LINES.
# import os
# print("AT START - " , os.getcwd())
# src_path = os.getcwd()
# new_path = os.path.join(src_path ,'code') # path to the output-folder
# os.chdir(new_path) # gotten into the output
# print("entered main_model module")
# print("AFTER GETTING IN - " , os.getcwd())
#########################################################################################

from model import _3_get_word_vectors
tokenizer , model = _3_get_word_vectors.loadBERTModel()
######################################################################################################

import os
curr_folder = os.getcwd()
os.chdir("../")
src_path = os.getcwd()
new_path = os.path.join(src_path ,'data') # path to the output-folder
new_path = os.path.join(new_path ,'url_csv_files') # path to the output-folder
os.chdir(new_path) # gotten into the output
import pandas as pd
df = pd.read_csv("article_url_list.csv")
list_of_all_urls = df["url"].tolist()
os.chdir(curr_folder)

from  model import _1_preprocess_text
list_of_url_and_name = _1_preprocess_text.listOfNamesOfUrl(list_of_all_urls)


from model import main_pipeline
articles_not_parsed = []
######################################################################################################
# RUNNING THE 'main_func'
import os
curr_path = os.getcwd()
import os
from dotenv import load_dotenv
load_dotenv()
arangodb_username = os.getenv("arangodb_username")
arangodb_password = os.getenv('arangodb_password')
database_name = os.getenv('database_name')
article_keywords_collection = os.getenv('crawler_model_tracker')
arangoURL = os.getenv('arangoURL')

from pyArango.connection import Connection
conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

try:
    db = conn.createDatabase(name=database_name) #handles creation of db
except:
    db = conn[database_name]         # handles opening of created db
print(db)

try:
    articles_Collection_tracker = db.createCollection(name=article_keywords_collection) #creating a new collection on db = school
except:
    articles_Collection_tracker = db[article_keywords_collection] #connecting if already exists.









for file in list_of_url_and_name:

    article_url = file[0]
    article_name = file[1]

   # try:
    doc = articles_Collection_tracker[article_name]
    if doc['bert_parsed'] == True:
        print("already parsed by bert -> " + str(article_name))
        continue
  #  except:
    #    print("cound not access from db-crawler-model-tracker collection :-> " + str(article_name)) 
    #    continue



    
#    try:
    os.chdir(curr_path)
    db , articles_Collection =  main_pipeline.main_func(article_name , article_url , model , tokenizer)
    os.chdir(curr_path)
    doc = articles_Collection_tracker[article_name]
    doc['bert_parsed'] = True
    doc.save()
   # except:
  #      articles_not_parsed.append(article_url)
     #   os.chdir(curr_path)
    #    continue

######################################################################################################
# WRITING TO SECOND COLLECTION - KEYWORD : URLS ASSOCIATED WITH IT.

#try:
from database import database_queries
database_queries.map_keywords_to_urls_in_db(articles_Collection, db)
#except:
#    print("no new keyword-urls mapped")

###################################################################################################
#try:
from database import database_queries
database_queries.map_keywords_with_vectors_in_db()
#except:
#    print("no new keyword-vectors mapped")
####################################################################################################
print("###################################################################################")
#print("URLS GIVING WEB DRIVER ERROR : " , list_web_driver_error_files)
print("ARTICLES NOT PARSED : " , articles_not_parsed)
print("###################################################################################")
print("FULL CODE RAN SUCCESSFULLY")


