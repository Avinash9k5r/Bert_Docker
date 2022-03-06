

def filenames(article_name):
    article_filename = article_name
    output_filename = 'out_' + article_filename + '.csv'
    output_mapped_filename = 'out_mapped_' + article_filename
    output_mapped_filename2 = 'final_out_mapped_' + article_filename
    topics_csv_filename = 'holy-topics.csv'
    output_filename_clusters = 'clusters_' + article_filename +'.txt'
    return article_filename , output_filename , output_mapped_filename , output_mapped_filename2 , topics_csv_filename , output_filename_clusters

#article_filename , output_filename , output_mapped_filename , output_mapped_filename2 , topics_csv_filename , output_filename_clusters= filenames(article_name)



def convertFileToVar(article_filename):

    file = open(article_filename)                                                                      
    var = file.read()                                                                                   
    file.close()
    return var





def removespecialchars(var):                                          #return- 2 var 'text'          
    import re
    text = re.sub(r'[^a-zA-Z]',' ',var) #no-2
    text = re.sub(r'\s+',' ',text)
    text = text.lower()
    text = re.sub(r'\d',' ',text)
    
    text_copy_for_ner_spacy = text + ' ' # made a new copy of the immutable string object for use later on for NER using spacy.
    return text , text_copy_for_ner_spacy




def tokenizeAndRemoveStopwords(text , stop_words):                 #returns 1 list- 'filtered_text'
    import nltk 
    # from nltk.corpus import stopwords
    # nltk.download('stopwords')
    # nltk.download('punkt')

    # stop_words = stopwords.words('english') #do-1
    stop_words.extend(['us','etc','god','jesus','lord','evil','devil','man','israel','people','king','son','men','house','day','children','land','things','hand','earth','sons','son','jerusalem','city','father','bible','tlb'])

    sentences = nltk.sent_tokenize(text) #no-3
    sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    for i in range(len(sentences)): #no-4
        sentences[i] = [word for word in sentences[i] if word not in stop_words]

    #print(sentences)
    filtered_sentence = sentences
    return filtered_sentence



def lemmatize(filtered_sentence , lemmatizer):#returns 1 list of lematized-words
    import nltk 
    from nltk.stem import WordNetLemmatizer # LEMMATIZATION OVER FILTERED_WORDS
    try:
            lemmatizer = WordNetLemmatizer()

            lematized_list = []
            print("This is len of filtered_sentence -> " + str(len(filtered_sentence)))
            print("This is filtered_sentence -> " + str(filtered_sentence))
            for word in filtered_sentence[0]:
                lematized_list.append(lemmatizer.lemmatize(word ,  pos="v"))
            lematized_list_short = list(set(lematized_list))
            lematized_list_short = lematized_list ### wasnt here before. added here on monday morning.


            print(len(lematized_list))
            print(len(lematized_list_short))
            return lematized_list
    except:
        nltk.download('wordnet')

        lemmatizer = WordNetLemmatizer()

        lematized_list = []
        for word in filtered_sentence[0]:
            lematized_list.append(lemmatizer.lemmatize(word ,  pos="v"))
        lematized_list_short = list(set(lematized_list))
        lematized_list_short = lematized_list ### wasnt here before. added here on monday morning.


        print(len(lematized_list))
        print(len(lematized_list_short))
        return lematized_list



def writeToFile(lematized_list , text_copy_for_ner_spacy):
    import pandas as pd
    df = pd.DataFrame(lematized_list , columns=['lematized_list'])
    #print(df)
    df.to_csv('lematized_list.csv' , index = False)

    file = open('text_cpy_ner_spacy.txt' , "w")
    file.write(text_copy_for_ner_spacy)
    file.close()
#writeToFile(lematized_list , text_copy_for_ner_spacy)




