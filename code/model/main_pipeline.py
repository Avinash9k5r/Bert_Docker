def main_func(article_filename , article_url , model , tokenizer):
    
    import os  
    curr_folder = os.getcwd() # currently in code-folder(the folder where the program is supposed to run)
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'model') # path to the model-folder
    os.chdir(new_path) # gotten into the model-folder


    from  model import _1_preprocess_text

  #  article_filename , output_filename , output_mapped_filename , output_mapped_filename2 , topics_csv_filename , output_filename_clusters = _1_preprocess_text.filenames(article_name)

    ############################
    curr_folder = os.getcwd() # currently in model-folder(the folder where the program is supposed to run)
    os.chdir('../')  # now in code-folder
    os.chdir('../')  # now in src-folder(parent folder of all folders)
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'data') # path to the data-folder
    new_path = os.path.join(new_path ,'downloaded_articles') # path to the downloaded_articles-folder
    os.chdir(new_path) # gotten into the downloaded_articles


    ############################
    data = _1_preprocess_text.convertFileToVar(article_filename)     #get the entire text of the website from the txt file into local-variable.
    if data == "":  # if article is empty then move on.
        os.chdir('../')  # now in src-folder(parent folder of all folders) 
        os.chdir(curr_folder) # again gotten into the code-folder
        return
    ###
    ################ NOW WE WILL COME OUT OF HERE AND GO BACK INTO THE 'code'-FOLDER
 
    os.chdir(curr_folder) # again gotten into the model-folder
    ############################

    text , text_copy_for_ner_spacy = _1_preprocess_text.removespecialchars(data)   #1st lvl preprocessing- removing everything except letters from a-z & A-Z from the text. We need two seperate copies of this text later, so we make two copies.
    #print(text + "hello")
    filtered_sentence = _1_preprocess_text.tokenizeAndRemoveStopwords(text)   #2nd lvl preprocessing- tokenizing the text and removing the stop word tokens from it.
    #print(filtered_sentence)
    lematized_list = _1_preprocess_text.lemmatize(filtered_sentence)   #3 lvl preprocessing- lemmatizing the list of tokens(words) and putting them in a list: 'lematized_list'- this is the final output of preprocessing.
    lematized_list_cpy = lematized_list.copy()

    # 'lematized_list' IS THE FINAL LIST OF WORDS AFTER ALL PREPROCESSING IS DONE. THIS IS THE MAJOR OUTPUT FROM THIS MODULE.
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FILE - 02
    from model import _2_get_all_nouns_in_text

    sent = []
    ner_spacy_tokens_list = _2_get_all_nouns_in_text.POSBySpacy(text_copy_for_ner_spacy)   #getting a list of all nouns in the text(lematized_list) by performing POS by spacy library.
    list_noun_words = _2_get_all_nouns_in_text.getAllNounsFromText(sent , ner_spacy_tokens_list)   #taking the union of both the lists so that we have a good collection of all words in lematized_list which are considered as a noun by atleast on of NLTK or spacy.
    _2_get_all_nouns_in_text.printPOSOfAWordFromText(ner_spacy_tokens_list , sent , 'isaiah')   #this is just a test-function which tells us the POS of a certain word('ask' for example) in the lematized_list, this can be used to check what POS does a certain word is recognized as.   

    # 'list_noun_words' CONTAINS LIST OF ALL NOUN-WORDS IN THE TEXT. THIS IS THE MAJOR OUTPUT WE RECIEVED FROM THIS MODULE
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FILE - 03

    from model import _3_get_word_vectors
    final_list_of_used_words , X = _3_get_word_vectors.getBERTVectors(lematized_list , model , tokenizer) #this func builds the BERT-vector for every word which is there in our lematized_list of words. 'final_list_of_words_used' = list of words which are recognized by the BERT model properly without too much segregation. 'X' = the corresponding 2D list containing the 768 vector representaion of every word in 'final_list_of_words_used'
    df = _3_get_word_vectors.buildDFOfCurrentWordVectorRelation(final_list_of_used_words , X)  #building the dataframe for visualization of the words and thier corresponding vectors.
    #_3_get_word_vectors.writeToFile(final_list_of_used_words , X)


    # 'X' , 'final_list_of_used_words' ARE THE MAJOR OUTPUTS WE RECIEVE FROM THIS FILE.
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FILE - 04
    from model import _4_get_elbow_value
    knee_point_value =  _4_get_elbow_value.printElbowMethodGraph(X) #here we visualise the knee-point value from the graph obtained by performing elbow method on the word-vectors, and we obtain knee-point value in an automated way by using the kneed-algorithm.

    # 'knee_point_value' REPRESENTS THE NO OF CLUSTERS OUR WORD-VECTORS SHOULD IDEALLY BE GROUPED IN. THIS IS THE MAJOR OUTPUT FROM THIS FILE.
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FILE - 05
    from model import _5_clusterize_and_get_keywords_from_each_cluster
    km , y = _5_clusterize_and_get_keywords_from_each_cluster.makeKClusters(knee_point_value , X) 
    final_list_of_used_words , X = _5_clusterize_and_get_keywords_from_each_cluster.removeAllWordsExceptNounsFromDF(final_list_of_used_words , X , list_noun_words)
    
    # now we keep the dataframe of word-vector relation for future use.
    import pandas as pd
    df_word_vectors = pd.DataFrame(X)
    df_word_vectors['word'] = final_list_of_used_words
    final_list_of_used_words_save = list(final_list_of_used_words) # making a copy as we need it later on, and the orignal will be changed.
    
    
    closest_overall_output_words , words_by_cluster_no , final_list_of_used_words , X , list_all_words = _5_clusterize_and_get_keywords_from_each_cluster.getTopNounsFromEachCluster(km , final_list_of_used_words , X  , lematized_list_cpy , num_of_clusters = knee_point_value)
    final_1st_lvl_out_listof_words , words_by_cluster_no, words_by_cluster_no_with_distances = _5_clusterize_and_get_keywords_from_each_cluster.mergeNounsFromEachCluster(words_by_cluster_no , list_all_words)
    out_words_list_for_mapping = list(set(final_1st_lvl_out_listof_words))

    #####################################################################################################
    curr_folder = os.getcwd() # currently in model-folder(the folder where the program is supposed to run)
    os.chdir('../')
    os.chdir('../')  # now in src-folder(parent folder of all folders)
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'output') # path to the output-folder
    new_path = os.path.join(new_path ,'all_files_keyword_vectors') # path to the output-folder
    os.chdir(new_path) # gotten into the output

    
    df_all_cluster_keywords = pd.DataFrame()
    print("len out_word_list_mapping -> " + str(len(out_words_list_for_mapping)))
    for word in out_words_list_for_mapping:
        try:
            idx = final_list_of_used_words_save.index(word) 
        except:
            continue
        df_row = df_word_vectors.iloc[[idx]]
        df_all_cluster_keywords = pd.concat([df_all_cluster_keywords, df_row])

    filenm = article_filename + ".csv"    
    df_all_cluster_keywords.to_csv(filenm)

    # now the keyword-vector file is saved locally, now we push it to  s3.
    
   


    ################ NOW WE WILL COME OUT OF HERE AND GO BACK INTO THE 'code'-FOLDER

    os.chdir(curr_folder) # again gotten into the model-folder
    os.chdir('../') # getting into the code-folder


    ######################################################################################################
    #WRITING TO DATABASE , COLLECTION - 'articles-collection'
    from database import database_queries
    db , articles_Collection = database_queries.write_url_clusters_to_db(words_by_cluster_no_with_distances, article_filename, article_url)


    return db , articles_Collection
