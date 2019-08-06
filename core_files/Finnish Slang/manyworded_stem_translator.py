import pickle
from lemmatizers import lemmatize_nominal,lemmatize_verb

group1 = pickle.load(open('manyworded_entries/manyword_entries_g1','rb'))
group1_second_members = pickle.load(open('manyworded_entries/manyword_entries_g1_second_pair_members','rb'))
group1_verbs = pickle.load(open('manyworded_entries/manyword_entries_g1_verbs','rb'))

group2 = pickle.load(open('manyworded_entries/manyword_entries_g2','rb'))
#!!! this should be a dictionary.
group2_last_words = pickle.load(open('manyworded_entries/manyword_entries_g2_last_words','rb'))

group3 = pickle.load(open('manyworded_entries/manyword_entries_g3','rb'))
group3_layer_2 = pickle.load(open('manyworded_entries/manyword_entries_g3_layer_2','rb'))

group4 = pickle.load(open('manyworded_entries/manyword_entries_g4','rb'))
#!!! this shoudl be a dictionary.
group4_last_words = pickle.load(open('manyworded_entries/manyword_entries_g4_last_words','rb'))


#!!! what if you have a manyworded instance separated by a comma? e.g. 'voi, ei!' - I could see this causing some problems with the highlighting function

def manyworded_stem_translator(candidate,history,text_instance):
    # First, we need to see if it is in group 1. First, let's see if the current word would be a second word in one of those pairs.
    # I've assumed that the second word, which is the argument of the verb pair, will always have the same form. If I need to do
    # lemmatization work with it, then I would need to slightly redesign this function. But it would be a doable adjustment - I would just
    # do a set-overlap test with this first 'if' statement. 
    if candidate in group1_second_members:
        # what if some of the olla verbs allow for 'na' endings as well . . .?
        # Ok. If it is, then we can see if the previous word is one of the group1_verbs:
        if set(lemmatize_verb(history[len(history)-1])) & set(group1_verbs):
            # It was! Let's grab their intersection.
            manyworded_candidate = list( set(group1_verbs).intersection(set(lemmatize_verb(history[len(history)-1]))) )[0]
            manyworded_candidate = manyworded_candidate + ' ' + candidate
            # This should give us the manyworded stem. I assume that each of these expressions is composed only of two words.
            # So we should see something like "puhua kreikaa" coming out of the woodwork here.
            if manyworded_candidate in group1:
                # add her up!
                answers = group1[manyworded_candidate]
                lemma = manyworded_candidate
                instance = history[len(history)-1] + ' ' + candidate

                return({(lemma,instance):answers})
    # Now let's see if it's in group2 - left branching madness.
    #!!! actually - watch out - you might be double-lemmatizing. 
    if candidate in group2_last_words:
     
        # I assume there will only be one match anyway. 
        # Ok, so match is the final word of a group2 entry that matches up with our current word.
        # (this line is not necessary in the current implementation, I'm effectively just renaming the variable.)
        match =  candidate
        # For every idiom that word is a part of, let's see if the history matches up with it. If it does, then we have a match.
        for idiom in group2_last_words[match]:
            print('the idiom is')
            print(idiom)
            good_match = True
            for i in range(len(idiom.split(' '))-1):
                corresponding_word_in_history = history[(len(history)-1)-i]
                split_idiom = idiom.split(' ')
                # trim off the last word - we've already checked for that.
                split_idiom = split_idiom[0:len(split_idiom)-1]
                corresponding_word_in_idiom = split_idiom[(len(split_idiom)-1)-i]

                print(" %s in histroy vs %s in idiom "%(corresponding_word_in_history,corresponding_word_in_idiom))

                if corresponding_word_in_idiom not in set(lemmatize_nominal(corresponding_word_in_history)):
                    #uh-oh, looks like there was a mismatch :( 
                    good_match = False
                    break
            if good_match:
                # add her up!
                lemma = idiom
                instance = ' '.join(history[len(history)-(len(idiom.split(' '))-1):]) + ' ' + text_instance
                answers = group2[idiom]
                return({(lemma,instance):answers})
    
    # Now let's see if it's in group 3. 
    if candidate in group3:
        # add her up!
        entry = group3[candidate]
        answers = group3_layer_2[entry]
        lemma = entry
        instance = text_instance
        return({(lemma,instance):answers})
        
    # Now let's see if it's in group 4.

    if candidate in group4_last_words:
        print('no yeah, it was in group 4 tho lol')
        for idiom in group4_last_words[candidate]:
            good_match = True
            for i in range(len(idiom.split(' '))-1):
                print(i)
                corresponding_word_in_history = history[ (len(history)-1)-i]
                
                split_idiom = idiom.split(' ')
                # trim off the last word - we've already checked for that.
                split_idiom = split_idiom[0:len(split_idiom)-1]
                corresponding_word_in_idiom = split_idiom[(len(split_idiom)-1)-i]
                print(" %s in histroy vs %s in idiom "%(corresponding_word_in_history,corresponding_word_in_idiom))

                if corresponding_word_in_history != corresponding_word_in_idiom:
                    good_match = False
                    break

            if good_match:
                # add her up! the lemma and the instance should be the same for this kind of entry. . . or maybe not. maybe you should change that.
                answers = group4[idiom]
                return({(idiom,idiom):answers})

    return None 


## Now let's test this function

# group 4 entry
history_g4 =['haha','ok','nope','ladata','lyijyä']
answer = manyworded_stem_translator('naamariin',history_g4,'naamariin')
print('ok, here we go, g4:')
print(answer)

# group 3 entry
answer = manyworded_stem_translator('bloukkaus',history_g4,'bloukkaudella')
print(answer)

# group 2 entry

print('\n')
#  !!! black out & bongi muna . . . why isn't bongi muna there in group 2?
history_g2 = ['haha','ok','wtf','lol','ikuinen']
answer = manyworded_stem_translator('kaupunki',history_g2,'kaupungissa')
print(answer)

# group 1 entry

print('group one, here we go!')
history_g1 = ['you','know','that\'s','not','soitin']
answer = manyworded_stem_translator('poskea',history_g1,'poskea')

print(answer)

