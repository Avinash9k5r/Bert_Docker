
def get_query_from_db():
    
    word_map_dictionary = {}
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    keyword_to_url_collection = os.getenv('keyword_url_collection')
    arangoURL = os.getenv('arangoURL')

    from pyArango.connection import Connection
    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    db = conn[database_name]   

    articles_Collection = db[keyword_to_url_collection]

    aql = "FOR x IN keyword_to_url_collection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult:
        word_map_dictionary.update({entry.get('KEYWORD') : entry.get('URL_ARRAY')})

    dict_of_keywords_with_no_of_urls_associated = {}

    for word in word_map_dictionary:
        dict_of_keywords_with_no_of_urls_associated.update({word : len(word_map_dictionary.get(word))})

    return word_map_dictionary

###################################################################################################################################
def get_list_of_filenames_of_urls():
   

    list_of_filenames_generated = {}
    
    import os
    print(os.getcwd())
    
    curr_path = os.getcwd()
   # os.chdir('../')
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'data') # path to the output-folder
    new_path = os.path.join(new_path ,'url_csv_files') # path to the output-folder
    os.chdir(new_path) # gotten into the output
    print(os.getcwd())


    import pandas as pd
    df = pd.read_csv('article_url_list.csv')
    urls = df['url'].tolist() 

    for url in urls:
        import re                                           
        filteredurl = re.sub(r'[^a-zA-Z]',' ',url)
        filteredurl = re.sub(r' ' , '_',filteredurl)
        filename =  "_" + filteredurl + ".txt"
        
        list_of_filenames_generated.update({url : filename})


    os.chdir(curr_path)
    
    return list_of_filenames_generated





