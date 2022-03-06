
def write_url_clusters_to_db(words_by_cluster_no_with_distances , article_name , article_url):

    ##################################################################################################
    #Writing to a database.
    
    db_doc = []
    i = 1
    for array in words_by_cluster_no_with_distances:
            
        cluster_name = str(i)
        new_tup = (article_name , article_url , cluster_name , array)
        
        db_doc.append(new_tup)
        
        i += 1
    
    #################################################################################################
    import os
    from dotenv import load_dotenv
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    article_keywords_collection = os.getenv('article_keywords_collection')
    arangoURL = os.getenv('arangoURL')

    from pyArango.connection import Connection
    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=article_keywords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[article_keywords_collection] #connecting if already exists.
    #################################################################################################
    
    for (article_name , article_url, cluster_name, cluster_keywords) in db_doc:
       doc = articles_Collection.createDocument()
       
       doc['ARTICLE_NAME'] = article_name
       doc['ARTICLE_URL'] = article_url
       doc['CLUSTER_NO'] = cluster_name
       doc['CLUSTER_KEYWORDS'] = cluster_keywords
       doc._key = ''.join([article_name, cluster_name]) 
       print(''.join([article_name, cluster_name]))
       try:
           doc.save()
       except:
           pass
        


    return db , articles_Collection



######################################################################################################################
def map_keywords_to_urls_in_db(articles_Collection , db):


    all_doc_all_clusters = []

    for article in articles_Collection.fetchAll():
        for word in article['CLUSTER_KEYWORDS']:
            all_doc_all_clusters.append(word[0])

    #print(all_doc_all_clusters)    



    set_all_words = list(set(all_doc_all_clusters))
    #print(set_all_words)



    word_map_dictionary = {}
    for word_first in set_all_words:
        lis = []
        for article in articles_Collection.fetchAll():
            for word_second_idx in range(len(article['CLUSTER_KEYWORDS'])):
                if word_first == article['CLUSTER_KEYWORDS'][word_second_idx][0]:
                    lis.append([article['ARTICLE_URL'] , article['CLUSTER_KEYWORDS'][word_second_idx][1] , article['CLUSTER_KEYWORDS'][word_second_idx][2]])
        # lis = list(set(lis))
            
            word_map_dictionary.update({word_first : lis})



    #print(word_map_dictionary)


    ######################################################################################################
    # CONNECTING TO SECOND COLLECTION - 'keyword_to_url_collection'
    try:
        articles_Collection = db.createCollection(name="keyword_to_url_collection") #creating a new collection on db = school
    except:
        articles_Collection = db["keyword_to_url_collection"] #connecting to 'keyword_to_url_collection' if already exists.


    for keyword , url_array in word_map_dictionary.items():
        doc = articles_Collection.createDocument()
        
        doc['KEYWORD'] = str(keyword)
        doc['URL_ARRAY'] = url_array
        doc._key = str(keyword)

        try:
            doc.save()
        except:
            pass




def map_keywords_with_vectors_in_db():  
    import pandas as pd      
    import os
    from dotenv import load_dotenv
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    keyword_url_collection = os.getenv('keyword_url_collection')
    arangoURL = os.getenv('arangoURL')

    from pyArango.connection import Connection
    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=keyword_url_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[keyword_url_collection] #connecting if already exists.
    #################################################################################################
    

    word_map_dictionary = {}  # { 'word': [['url', cluster-center-dist, freq]]  }
    list_of_all_keywords = []

    aql = "FOR x IN keyword_to_url_collection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult:
        word_map_dictionary.update({entry.get('KEYWORD') : entry.get('URL_ARRAY')})
        list_of_all_keywords.append(entry.get('KEYWORD'))
        
    word_vectors_list = []     # [[word , 768vector] , [word , [768vector] , ... ]


    #go to output\all_keyword_vectors
    import os
    curr_folder = os.getcwd()
    os.chdir("../")
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'output') # path to the output-folder
    new_path = os.path.join(new_path ,'all_files_keyword_vectors')
    os.chdir(new_path) 
    
    df_all_cluster_keywords = pd.DataFrame()    
    for keyword in list_of_all_keywords:
        matrix = word_map_dictionary.get(keyword)

        import re        
        url = matrix[0][0]                               
        filteredurl = re.sub(r'[^a-zA-Z]',' ',url)
        filteredurl = re.sub(r' ' , '_',filteredurl)
        filename =  "_" + filteredurl + ".txt" + ".csv"

        print(keyword)
        df = pd.read_csv(filename)
        list_words = df['word'].tolist()
        try:
            idx = list_words.index(keyword)
            df_row = df.iloc[[idx]]
            print(type(df_row))
            df_all_cluster_keywords = pd.concat([df_all_cluster_keywords, df_row])
        except:
            pass

    os.chdir("../")
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'all_keyword_vectors') # path to the output-folder
    os.chdir(new_path)
    df_all_cluster_keywords.to_csv("all_keywords_vectors.csv" , index = False)
    # put this file(.csv) onto s3, and pull it firstly when trying to access capi or ui code.
    from crawler import s3_functions
    bucketname = os.getenv('bucketname')
    returncode , key = s3_functions.upload_my_file(bucketname, "all_keyword_vectors", "all_keywords_vectors.csv", "all_keywords_vectors.csv") # returns key for that file ipload.
    print(returncode) # true is successfull updation of s3 happens.
    os.chdir(curr_folder)

