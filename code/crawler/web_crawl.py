def crawl_all_urls_in_list(urls):

    import os
    from dotenv import load_dotenv
    load_dotenv()
####################################################################################
    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    article_keywords_collection = os.getenv('crawler_model_tracker')

    from pyArango.connection import Connection
    conn = Connection(username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=article_keywords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[article_keywords_collection] #connecting if already exists.

    list_of_already_crawled_urls = []
    for article in articles_Collection.fetchAll():
        list_of_already_crawled_urls.append(str(article['crawled_url']))
   
###################################################################################
    from selenium import webdriver
    import os
    curr_folder = os.getcwd()

    webdriver_path =  os.path.join(curr_folder ,'chromedriver.exe')
    driver = webdriver.Chrome(webdriver_path) #run once only. will do the job for all urls
    # options = webdriver.ChromeOptions()
    # options.add_argument('--disable-extensions')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(chrome_options=options)

    list_web_driver_error_files = []
    list_of_filenames_generated = []
    ######################################################################################################################
    for url in urls:

        ## check wheather it is to be crawled or not.-> from db.
        if url in list_of_already_crawled_urls: # don't crawl if already crawled.
            continue

        try:
            driver.get(url)
            paragraphs = driver.find_elements_by_tag_name('p') # getting all <p> elements from the website.

            import re                                           # naming the file
            filteredurl = re.sub(r'[^a-zA-Z]',' ',url)
            filteredurl = re.sub(r' ' , '_',filteredurl)
            filename =  "_" + filteredurl + ".txt"
            list_of_filenames_generated.append([filename , url])
        except:                                                 # sometimes due to error, webdriver needs to be restarted.
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-extensions')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(chrome_options=options)
            list_web_driver_error_files.append(url)
            
            paragraphs = driver.find_elements_by_tag_name('p') 

            import re
            filteredurl = re.sub(r'[^a-zA-Z]',' ',url)
            filteredurl = re.sub(r' ' , '_',filteredurl)
            filename = "_" + filteredurl + ".txt"
            list_of_filenames_generated.append([filename , url])

        
        
    ######################################################################################################    
        # now upload the crawled file to s3 here.
        file = open(filename , 'w')
        file.write("")
        file.close()
        file = open(filename , 'a')
        try:
            for paragraph in paragraphs:
                file.write(paragraph.text.encode().decode('ascii', 'ignore'))
                file.write('\n')
        except:
            pass
        file.close() 
        
        # till now it is written to local filesystem, now we write to s3
        from crawler import s3_functions
        bucketname = os.getenv('bucketname')
        returncode , key = s3_functions.upload_my_file(bucketname, "downloaded_articles", filename, filename) # returns key for that file ipload.
        print(returncode) # true is successfull updation of s3 happens.
        s3_url = s3_functions.getUrl(key , bucketname)
        

        # make an entry of it in databse collection.
        docu = articles_Collection.createDocument()
        docu['crawled_url'] = str(url)
        docu['s3_object_presigned_url'] = str(s3_url)
        docu['bert_parsed'] = False
        docu['filename'] = filename
        docu._key = str(filename)
        try:
            docu.save()
        except:
          pass 
        
        # now we remove the locally saved crawled file, as we no longer need it after pushing it to s3.
        files_in_directory = os.listdir(os.getcwd())
        filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
        for file in filtered_files:
            path_to_file = os.path.join(os.getcwd(), file)
            os.remove(path_to_file)

        print("CRAWLING :-> URL : " , url)

    ######################################################################################################################

    os.chdir('../')  # now in src-folder(parent folder of all folders) 
    os.chdir(curr_folder) # again gotten into the model-folder
    
    return list_of_filenames_generated , list_web_driver_error_files




def get_list_of_urls():
    import os
    curr_folder = os.getcwd() # currently in model-folder(the folder where the program is supposed to run)
    os.chdir('../')  # now in src-folder(parent folder of all folders)
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'data') # path to the data-folder
    new_path = os.path.join(new_path ,'url_csv_files') # path to the url_csv_files-folder
    os.chdir(new_path) # gotten into the url_csv_files
    ############
    import pandas as pd
    df = pd.read_csv('article_url_list.csv')
    urls = df['url'].tolist() 
    #print(urls)
    ############
    os.chdir(curr_folder) # again gotten into the model-folder    

    return urls
