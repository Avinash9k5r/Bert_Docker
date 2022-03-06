######################################################################################################
# HERE WE CRAWL ALL THE WEBSITES IN URL-LIST  


import os
curr_folder = os.getcwd() # currently in code-folder(the folder where the program is supposed to run)
from crawler import web_crawl , s3_functions
urls = web_crawl.get_list_of_urls()




src_path = os.getcwd()
new_path = os.path.join(src_path ,'crawler') 
os.chdir(new_path) 
from crawler.web_crawl import crawl_all_urls_in_list
list_of_filenames_generated , list_web_driver_error_files = crawl_all_urls_in_list(urls)

print("A")

os.chdir("../")
os.chdir("../")
src_path = os.getcwd()
new_path = os.path.join(src_path ,'data') # path to the data-folder
os.chdir(new_path)
from dotenv import load_dotenv
load_dotenv()
bucketname = os.getenv('bucketname')
s3_functions.downloadDirectoryFroms3(bucketname , "downloaded_articles")


print("B")



import os
os.chdir(curr_folder) # again gotten into the code-folder(just as a precaution).

import pandas as pd
df1 = pd.DataFrame(list_of_filenames_generated , columns=['url_name' , 'url_val'])
df2 = pd.DataFrame(list_web_driver_error_files , columns=['list_web_driver_error_files'])

df1.to_csv("list_of_filenames_generated.csv" , index = False)
df2.to_csv("list_web_driver_error_files.csv" , index = False)

######################################################################################################