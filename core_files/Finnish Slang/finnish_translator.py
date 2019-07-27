"""
This file represents the highest level control point in the library. 
It makes use of the lemmatizers and the libraries to identify slang words in a given stream of text,
and it returns their translations. 
"""

import pickle
import re
from lists_and_dictionaries import common_spoken_language_words
from lemmatizers import lemmatize_nominal,lemmatize_verb
from basic_word_manipulation import remove_copies

  # loading in corpus
"""
file = open("assign1.3_out","rb")
sanalista = pickle.load(file)
file.close()

med = {}

for fru in sanalista:
    med.update(fru)

for old_key in med:
    new_key = old_key.lower()
    med[new_key] = med.pop(old_key)

"""

def translate_finnish(text,reference):
    
    # First, tokenizing it into words.
    text = re.sub("[,\.\(\)\"\!\n\-\?\']"," ",text)
    text = text.lower()
    tokenized_text = re.split(" ",text)
    
    # Attenuating our text slightly
    L = []

    for token in tokenized_text:
        if token == "":
            pass
        elif re.search("[0-9]",token):
            pass
        elif token in common_spoken_language_words:
            print("found that %s is a common spoken language thing"%token)
        else:
            L.append(token)
    
    tokenized_text = L


    # searching for slangwords

  

    # checking words
    
    # creating a list of lists - each word in the corpus will now be represented as 
    # a list of all possible lemmas that could have been derived from that word.
    master_list = []
    print(tokenized_text)
    for token_2 in tokenized_text:
        mediating_list = list(lemmatize_nominal(token_2))
        mediating_list +=  list(lemmatize_verb(token_2))
        mediating_list = [token_2]+mediating_list
        ###!!! there may be consequences to having the found form of the word not being the first one on the list... 
        ## maybe make sure that remove copies will leave it in the first slot?
        mediating_list = remove_copies(mediating_list)
        master_list.append(mediating_list)

    print(master_list)

    # If any of those possibilities happens to be a word in our slang dictionary, then we add it to our answers.
    answers = []
    for list_of_possible_lemmas in master_list:
        for possibility in list_of_possible_lemmas:
            print (possibility)
            if possibility in reference:
                # list_of_possible_lemmas[0] should point to the word as it was originally seen in the text. This allows us to go back and highlight it.
                
                # also, to make this dictionary more parsable in the javascript, I need to make sure that the up and down votes are represented both as strings.
                transformed_answer_content = []
                answer_content = reference[possibility]
                for given_answer in answer_content:
                    transformed_answer = list(given_answer)
                    transformed_answer[2] = str(transformed_answer[2])
                    transformed_answer[3] = str(transformed_answer[3])
                    transformed_answer_content.append(tuple(transformed_answer))

                answers.append({ (possibility, list_of_possible_lemmas[0])  : transformed_answer_content })
    

    return answers





#print(translate_finnish("euforia on paras juttu",med))
#print(sanalista)


## do lower case on the keys of the dictionary