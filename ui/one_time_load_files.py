
#THIS MODEULE CONTAINS THOSE FUNCTIONS WHICH DOWNLOAD IMP DATA, AND MUST TO BE LOADED ONLY ONCE FOR GOOD SPEED.

def one_load_files():
    #####################################################################
    # LOADING THE LEMMATIZER HERE, AS IT SHOULD BE LOADED ONLY ONCE AT THE START!
    import nltk 
    from nltk.stem import WordNetLemmatizer # LEMMATIZATION OVER FILTERED_WORDS
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = stopwords.words('english') #do-1

    return lemmatizer , stop_words
    #####################################################################