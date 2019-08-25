"""
This file helps sort out our database. It's to be used after everything's been scraped.

What it does is takes a list of words that I want to be exact matches, and then it 
separates those from the main database-dictionary, and puts them in a separate dictionary.
This allows these entries to be handled differently, so that my app will only count
them as a match if the token matches with them EXACTLY. 

"""

import pickle
database_file = open('resources/slang_database_v2','rb')
database = pickle.load(database_file)
exact_matches = ["nä","voa","ke","tää","koa","ko","ka","kaa"]
exact_matches = set(exact_matches)

exact_matches_dict = {}

for exact_match in exact_matches:
    exact_matches_dict[exact_match] = database[exact_match]
    del database[exact_match]


pickle_out = open("resources/slang_database",'wb')
pickle.dump(database,pickle_out)


pickle_out_2 = open("resources/exact_matches","wb")
pickle.dump(exact_matches_dict,pickle_out_2)
