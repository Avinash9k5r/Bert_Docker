
def searchFunc(word_map_dictionary , inputstr , lemmatizer , stop_words , list_of_filenames_generated):
    def search_best_url_from_keywords(list_of_words_as_input , word_map_dictionary):
        ############################################################################
        # we are using 'word_map_dictionary' here as the only input here below.
        ########################################################################
        final_url_mappings = {}

        for word_1 in list_of_words_as_input:
            if word_1 not in word_map_dictionary:
                continue

            array_of_urls_and_dist = word_map_dictionary.get(word_1)

            for word in array_of_urls_and_dist:

                if word[0] in final_url_mappings:
                    word_freq_dict.append([word_1 , word[2]])
                    val = final_url_mappings.get(word[0])[0]
                    avg_dist = ((final_url_mappings.get(word[0])[1] * val) + word[1]) / (val+1) 
                    val += 1
                    final_url_mappings.update({word[0] : [val , avg_dist , word_freq_dict]})
                else:   
                    word_freq_dict = [word_1 , word[2]]
                    final_url_mappings.update({word[0] : [1 , word[1] , word_freq_dict]})
        #########################################################################
        final_url_mappings
        #########################################################################
        # now we sort accordign to priority : frequency first and closest distance second.
        sorted_tuples = sorted(final_url_mappings.items(), key=lambda item: (-1*item[1][0] , item[1][1]))
        #########################################################################
        return sorted_tuples

    def search(word_map_dictionary , inputstr , lemmatizer , stop_words):
        search_string = inputstr
        #processing the search_string to keywords:
        import _1_preprocess_text
        text , text_copy_for_ner_spacy = _1_preprocess_text.removespecialchars(search_string)
        filtered_sentence = _1_preprocess_text.tokenizeAndRemoveStopwords(text , stop_words)
        lematized_string = _1_preprocess_text.lemmatize(filtered_sentence , lemmatizer)
        ###
        keywords_to_search = lematized_string


        best_urls_tuple = search_best_url_from_keywords(keywords_to_search , word_map_dictionary)


        retlist = []
        for url in best_urls_tuple:
            if len(best_urls_tuple) == 0:
                break
            retlist.append(url)
        

        if len(retlist) > 10:
            retlist = retlist[ : 10]


        return retlist


        
        
    #########################################################################################################################################    

    ###########################################################################################################################################
    retlist =  search(word_map_dictionary , inputstr , lemmatizer , stop_words)
    ###########################################################################################################################################

    list_of_names_of_url = []

    for urllist in retlist:
        list_of_names_of_url.append(list_of_filenames_generated.get(urllist[0]))
    
    list_of_paras = []
    #############################################################################################################
    import os
    curr_folder = os.getcwd() # currently in code-folder(the folder where the program is supposed to run)
    print(os.getcwd())
    os.chdir("../")
    src_path = os.getcwd()
    new_path = os.path.join(src_path ,'data')
    new_path = os.path.join(new_path ,'downloaded_articles') # path to the downloaded_articles-folder
    os.chdir(new_path) # gotten into the downloaded_articles
    
    if len(list_of_names_of_url) == 0:
        list_of_paras.append("NOTHING TO SHOW")
        retlist.append(["NO RESULTS"])

    for nameofurl in list_of_names_of_url:
        file = open(nameofurl)                                                                      #@!
        var = file.read()                                                                                  #@!  
        file.close()
        para = var                        #var[ : 1000] + ".................................."
        list_of_paras.append(para)


    os.chdir(curr_folder)  # now in src-folder(parent folder of all folders)     
    ######################################################################################################
    return retlist , list_of_paras
    
        


# line 80