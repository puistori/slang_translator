"""
This file represents the highest level control point in the library. 
It makes use of the lemmatizers and the libraries to identify slang words in a given stream of text,
and it returns their translations. 

What this function returns in a more technical sense, is a list of mappings between lemma-instance tuples as the key
and lists of answers as the values.

e.g.  [ (lemma, instance) : [ [definition 1, examples, upvotes etc. . . ] , [definition 2, examples, upvotes etc. . . ] ] , (lemma2, instance) : ... ]

"""

import pickle
import re
from lists_and_dictionaries import common_spoken_language_words
from lemmatizers import lemmatize_nominal,lemmatize_verb
from basic_word_manipulation import remove_copies
from manyworded_stem_translator import manyworded_stem_translator

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

def translate_finnish(text,reference,databases,exact_matches=None,ignore_us=None):
    
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
        ### !!! There is a problem with this condition and the one after that !!!!!! 
        ### they don't allow these words to be part of the history of the sentence, which
        ### won't allow them to be recognized if they form part of a manyworded stem.
        elif token in common_spoken_language_words:
            print("found that %s is a common spoken language thing"%token)
        elif ignore_us != None and token in ignore_us:
            #These are hardcoded corrections for misslematizations.
            pass
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
        # First, we want to see if it's an exact match. If it is, we don't need to try to lemmatize it!
        if token_2 in reference:
            mediating_list = []
        elif exact_matches != None and token_2 in exact_matches:
            mediating_list = []
            print("this did go here! \n\n\n\n\n yes it did!")
        else:
            print("ok ok ok ok  but it didn't go here, did it . . ?")
            try:
                mediating_list = list(lemmatize_nominal(token_2))
            except:
                print("Something went wrong trying to lemmatize a word as a nominal")
                print("The word: %s"%(token_2))
            try:
                mediating_list +=  list(lemmatize_verb(token_2))
            except:
                print("Something went wrong trying to lemmatize a word as a verb")
                print("The word: %s"%(token_2))
        mediating_list = [token_2]+mediating_list
        ###!!! there may be consequences to having the found form of the word not being the first one on the list... 
        ## maybe make sure that remove copies will leave it in the first slot?
        mediating_list = remove_copies(mediating_list)
        master_list.append(mediating_list)

    print(master_list)

    # If any of those possibilities happens to be a word in our slang dictionary, then we add it to our answers.
    answers = []
    # we want to keep track of a stack of about 10 words or so, so that we can identify manyword-stems.
    # History will be treated as a queue - with filo ordering. It will begin stocked with dummy words.
    history = ["@x@","@x@","@x@","@x@","@x@","@x@","@x@","@x@","@x@","@x@"]
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

                # this object is a lemma-instance tuple mapped to a list of answers. 
                answers.append({ (possibility, list_of_possible_lemmas[0])  : transformed_answer_content })
            # Now let's check to see if it's in the "exact matches" category
            elif exact_matches != None and possibility in exact_matches and possibility == list_of_possible_lemmas[0]:
                #also, to make this dictionary more parsable in the javascript, I need to make sure that the up and down votes are represented both as strings.
                transformed_answer_content = []
                answer_content = exact_matches[possibility]
                for given_answer in answer_content:
                    transformed_answer = list(given_answer)
                    transformed_answer[2] = str(transformed_answer[2])
                    transformed_answer[3] = str(transformed_answer[3])
                    transformed_answer_content.append(tuple(transformed_answer))

                # this object is a lemma-instance tuple mapped to a list of answers. 
                answers.append({ (possibility, list_of_possible_lemmas[0])  : transformed_answer_content })
            else:
                # Now we need to check if it's part of a maniworded stem. 
                try:
                    print('did this happen first?')
                    print(history)
                    manyword_stem = manyworded_stem_translator(possibility,history,list_of_possible_lemmas[0],databases) 
                    if manyword_stem != None:
                        answers.append(manyword_stem)

                except Exception as e:
                    print("Something went wrong when checking for a manyword-stem")
                    print("Current Word: %s"%list_of_possible_lemmas[0])
                    print("History: %s"%history)
                    print(e)
                    
        # regardless of the result, we need to push this into the history. 
        print(" or did this?")
        history.append(list_of_possible_lemmas[0])
        history.pop(0)

    return answers


#print(sanalista)

print(lemmatize_nominal('turkat'))
## do lower case on the keys of the dictionary