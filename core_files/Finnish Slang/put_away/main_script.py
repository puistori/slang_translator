from lemmatizers import *
import re
import pickle
from scraper import *
import time as t
import os
from lists_and_dictionaries import *

directory = "C:/Users/puistori/PycharmProjects/Finnish Slang"

if os.path.isfile("found_slang_words"):
    pickle_in = open("found_slang_words","rb")
    found_slang_words = pickle.load(pickle_in)
    print("found it!")
else:
    found_slang_words = {}

if os.path.isfile("probably_improper_word_forms"):
    pickle_in = open("probably_improper_word_forms","rb")
    probably_improper_word_forms = pickle.load(pickle_in)
    print("found it!")
else:
    probably_improper_word_forms = set()

if os.path.isfile("failed_searches"):
    pickle_in = open("failed_searches","rb")
    failed_searches = pickle.load(pickle_in)
    print("found it!")
else:
    failed_searches = set()


sanalista = pickle.load(open("minun_sanalista","rb"))

corpus = open("sata_lasissa.txt","rt",encoding="utf-8")
string = ""
for line in corpus:
    string += line


string = re.sub("[,\.\(\)\"\!\n\-\?\']"," ",string)
string = string.lower()
corpus = re.split(" ",string)



# Here is the attenuation stage. words that we know aren't any good are taken out immediately.
attenuated_corpus = []
for word_one in corpus:
    if word_one == "":
        pass
    elif re.search("[0-9]",word_one):
        pass
    elif word_one in common_spoken_language_words:
        print("found that %s is a common spoken language thing"%word_one)
    elif word_one in found_slang_words:
        print("already found %s in slang words"%word_one)
    elif word_one in probably_improper_word_forms:
        print("already found %s in improper word forms"%word_one)
    elif word_one in failed_searches:
        print("already found %s in failed searches "%word_one)
    elif word_one not in sanalista:
        attenuated_corpus.append(word_one)
    else:
        print("didn't know what to do with this one lol %s "%word_one)

print(corpus)

master_list = []
for word in attenuated_corpus:
    mediating_list = list(lemmatize_nominal(word))
    mediating_list = remove_copies(mediating_list)
    mediating_list +=  list(lemmatize_verb(word))
    mediating_list = remove_copies(mediating_list)
    mediating_list = [word]+mediating_list
    #mediating_list = tuple(mediating_list)
    master_list.append(mediating_list)




unidentified_words = []
for member in master_list:
    unidentified = True
    for possibility in member:
        if possibility == member[0]:
            pass
        elif possibility in sanalista:
            #print("The lemma, %s was found in the wordlist" %possibility)
            unidentified = False
            break
    if unidentified:
        #print("The following wordset was unidentified: %s"%member)
        unidentified_words.append(member)


"""
print(len(unidentified_words))
print("Printing the unidentified lemmas:")
for unidentified_thing in unidentified_words:
    print("The word %s was unidentified. below are the results."%unidentified_thing[0])
    print(unidentified_thing)
"""



# Ok, these are the words that will end up getting sent to the website.
search_requests = []
for unidentified in unidentified_words:
    request = remove_copies(unidentified)
    search_requests.append(request)

for request in search_requests:
    print(request)

def search_online(list_):
    found_slang_words = {}
    failed_searches = set()
    probably_improper_word_forms = set()
    for word in list_:
        print(" Ok, the word we are looking up is: %s"%word)
        try:
            print("we... we tried!")
            url = fetch_word_url(word)
            print(url)
            print(type(url))
            if isinstance(url,str):
                boolean,definition,examples = fetch_definition(url)
                if boolean:
                    found_slang_words[word] = (definition,examples)
                    for other_word in list_:
                        if other_word != word:
                            print("adding %s to the set lol"%other_word)
                            probably_improper_word_forms.add(other_word)
                    print("Found a definition!")
                    print(definition)
            else:
                print("Lol adding %s to the failed searches haha"%word)
                failed_searches.add(word)
                t.sleep(1)
        except:
            pass
    print("failed searches lol")
    print(failed_searches)
    print("improper word forms lol")
    print(probably_improper_word_forms)
    return(found_slang_words,failed_searches,probably_improper_word_forms)

def search_them_all(words):

    found_slang_words_master = {}
    failed_searches_master = set()
    probably_improper_word_forms_master = set()

    # To give you some impression of how long it will take
    wait_time = 0
    for word in words:
        print("here is a lemma entry: %s"%word)
        wait_time +=3
        for subword in word:
            wait_time += 1
    for lemma in words:
        print("About %s seconds left"%wait_time)
        wait_time -= (len(lemma)+3)
        found_slang_words,failed_searches,probably_improper_word_forms = search_online(lemma)
        for key in found_slang_words:
            found_slang_words_master[key] = found_slang_words[key]
        failed_searches_master.update(failed_searches)
        probably_improper_word_forms_master.update(probably_improper_word_forms)

    return(found_slang_words_master,failed_searches_master,probably_improper_word_forms_master)


found_slang_words_sub,failed_searches_sub,probably_improper_word_forms_sub = search_them_all(search_requests)

for key in found_slang_words_sub:
    if key not in found_slang_words:
        found_slang_words[key] = found_slang_words_sub[key]

failed_searches.update(failed_searches_sub)
probably_improper_word_forms.update(probably_improper_word_forms_sub)


print(found_slang_words)
print(failed_searches)
print(probably_improper_word_forms)

new_file = open("found_slang_words","wb")
pickle.dump(found_slang_words,new_file)
new_file.close()

new_file = open("probably_improper_word_forms","wb")
pickle.dump(probably_improper_word_forms,new_file)
new_file.close()

new_file = open("failed_searches","wb")
pickle.dump(failed_searches,new_file)
new_file.close()
