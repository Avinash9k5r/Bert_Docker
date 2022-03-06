from flask import Flask , render_template
from flask import request, jsonify
from flask.templating import render_template
from main_search_api import searchFunc
from get_arango_query_for_search_string import get_query_from_db
from get_arango_query_for_search_string import get_list_of_filenames_of_urls
import time
from flask_cors import CORS
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

##################################################################
from one_time_load_files import one_load_files
lemmatizer , stop_words = one_load_files()
##################################################################
speech_text = ''
##################################################################

##1-pull 'word_map_dictionary' once from db
# add arango connection here and do computations only but once.
word_map_dictionary = get_query_from_db()
list_of_fienames_generated = get_list_of_filenames_of_urls()
##################################################################

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


    
@app.route('/search', methods=['GET' , 'POST'])
def api_id():
    start = int(time.time()*1000)
    if 'input' in request.args:
        inputstr = str(request.args['input'])
    #else:
    #    return "Error: No input field provided. Please specify an input string."

    retdict = []

    global speech_text
    if speech_text != '':
        inputstr = str(speech_text)
        print(inputstr)
        speech_text = '' 
    
    retval , retval1 = searchFunc(word_map_dictionary , inputstr , lemmatizer , stop_words , list_of_fienames_generated)
    
    retdict = []
    for idx in range(len(retval)):
        retdict.append([retval[idx] , retval1[idx]])


    inputstr = inputstr.replace(' ', '_')
    end = int(time.time()*1000)
    print("time for search string to result generation = " , end - start)
    return render_template('resultUI.html', data=retdict , search_string = inputstr)





if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000) # 