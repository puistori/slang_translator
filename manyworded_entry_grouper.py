"""
The purpose of this file is to divide the many-worded entries into different groups that can be handled. Many-worded entries are entries
that are composed of more than one word, like "voi ei!". There are four groups that I've made:

1. These are pairs beginning with a recognizable verb. "puhua kreikaa" is a good example.

2. These are leftbranching noun phrases, like "poliittinen itsemurha"

3. These are either/or entries, where the entry is meant to cover either one word or another, like "siftata / shiftata"

4. These are whole idioms, like "voi ei!"
"""

#!!! There may be something wrong with how it groups words into group 2 - for some reason, words ending in muna don't end up there :(

import pickle
import re

sanalista = open('core_files/Finnish Slang/sanalista/kotus-sanalista_v1.xml','rt')

normal_words = []

for line in sanalista.readlines():
    q = re.search(r'(?<=<s>).*?(?=</s>)',line)
    # This is sloppy, I know. But the original file has 'out' as an entry in it for some reason. 
    # I don't want that, but I also don't want to alter the original file.
    if q and q.group(0) !='out':
        normal_words.append(q.group(0))

# Checking for membership is quicker in sets, so we'll use a set. 
normal_words = set(normal_words)


database = pickle.load(open('resources/slang_database','rb'))


double_lemmas = {}

other_count = 0
count = 0

group1_count = 0
group2_count = 0
group3_count = 0
group4_count = 0

# entries with just one word.
one_word_entries = {}

# Now, these dictionaries are full of entries that have more than one word.

# Group 1 is composed of verb pairs where the first member is a conjugatable verb, and the second member is an argument of the verb.
# For now, I am accepting only olla, saada, puhua, ottaa and soittaa ; this may be subject to change.
group1 = {}
group1_verbs = set(['olla','saada','puhua','ottaa','soittaa'])
group1_second_pair_members = set([])
# Group 2 is composed of left-branching nominal expressions. The last words maps the last word of an idiom to a list of idioms it's a part of.
group2 = {}
group2_last_words = {}
# Group 3 is composed of multi-key entries, like ' shiftata / siftata' which points to a definition of 'either one'
# This will be treated by putting in a 'second layer' - each individual word will be mapped to the compound lemma (e.g, 
#  'siftata' by itself will map to 'shiftata / siftata' and then that compound will map to the meaning.)
group3 = {}
group3_second_layer = {}
# Group 4 is composed of whole idioms and the like. A perfect match will be required. the last words maps the last word of an idiom to a list of idioms it's a part of.
group4 = {}
group4_last_words = {}




for key in database:
    # This first condition filters for all many-word entries. 
    if " " in key:

        if 'muna' in key or 'kauhistus' in key:
            print("yeah, it passed this way. what of it?")
            print(key)

        count += 1
        found = False
        # Now we need to figure out what sub-group they fall into.
        stem = key.split(' ')[0]
        # Filtering for words that start with a recognizable lemma. These words could fall into groups 1, 2, or 4.
        if stem in normal_words:

            if 'muna' in key or 'kauhistus' in key:
                print("yeah, it passed this way. part 1. what of it?")
                print(key)

            # It could belong to group 2, if the first word is an adjective
            if stem in ['pieni','iso'] or stem.endswith('inen'):
                group2_count += 1
                
                group2[key.replace('?','').replace('!','')] = database[key]
                if key.split(' ')[len(key.split(' '))-1] in group2_last_words:
                    group2_last_words[key.split(' ')[len(key.split(' '))-1]].append(key)
                else:
                    group2_last_words[key.split(' ')[len(key.split(' '))-1]] = [key]
                found = True
            # Group 1 is only taking specific verbs for the time being.
            elif stem in group1_verbs:

                group1_count += 1
                
                group1[key.replace('?','').replace('!','')] = database[key]
                group1_second_pair_members.add(key.split(' ')[1])
                found = True
            else:
                # In this case, we'll just punt it over to group 4. 
                group4_count += 1
                group4[key.replace('?','').replace('!','')] = database[key]
                if key.split(' ')[len(key.split(' '))-1] in group4_last_words:
                    group4_last_words[key.split(' ')[len(key.split(' '))-1]].append(key)
                else:
                    group4_last_words[key.split(' ')[len(key.split(' '))-1]] = [key]
                found = True
        # group 2 - searching for entries who end in a recognizable word.
        if key.split(' ')[len(key.split(' '))-1] in normal_words and found == False:
                
            if 'muna' in key or 'kauhistus' in key:
                print("yeah, it passed this way. part 2. what of it?")
                print(key)
                print(key.split(' ')[len(key.split(' '))-1])
            
                for word in normal_words:
                    if word == "out":
                        print("well, yeah I guess")
                        print(word)

            
                group2_count += 1
                
                group2[key.replace('?','').replace('!','')] = database[key]
                if key.split(' ')[len(key.split(' '))-1] in group2_last_words:
                    group2_last_words[key.split(' ')[len(key.split(' '))-1]].append(key)
                else:
                    group2_last_words[key.split(' ')[len(key.split(' '))-1]] = [key]
                found = True
        # group 3 - searching for entries containing a slash or a comma.
        if ',' in key or '\/' in key:
                group3_count += 1
                
                group3_second_layer[key] = database[key]
                for ele in re.split('(,|\/)', key):
                    group3[ele.replace('?','').replace('!','')] = key
                found = True
            
        # group 4
        if found == False:
                group4_count += 1
                if 'muna' in key or 'kauhistus' in key:
                    print("yeah, it passed this way into the second round. what of it?")
                    print(key)
                    print(key.split(' ')[len(key.split(' '))-1])
                group4[key.replace('?','').replace('!','')] = database[key]
                if key.split(' ')[len(key.split(' '))-1] in group4_last_words:
                    group4_last_words[key.split(' ')[len(key.split(' '))-1]].append(key)
                else:
                    group4_last_words[key.split(' ')[len(key.split(' '))-1]] = [key]

                found = True
            
    else:
        other_count +=1

print(count)
print(other_count)
#print("now by groups:")
#print(group1,group2,group3,group4)


g1 = open('manyworded_entries/manyword_entries_g1','wb')
pickle.dump(group1,g1)
g1.close()

g1_v = open('manyworded_entries/manyword_entries_g1_verbs','wb')
pickle.dump(group1_verbs,g1_v)
g1_v.close()


g1_second_pair_members = open('manyworded_entries/manyword_entries_g1_second_pair_members','wb')
pickle.dump(group1_second_pair_members,g1_second_pair_members)
g1_second_pair_members.close()


g2 = open('manyworded_entries/manyword_entries_g2','wb')
pickle.dump(group2,g2)
g2.close()


g2_last_words = open('manyworded_entries/manyword_entries_g2_last_words','wb')
pickle.dump(group2_last_words,g2_last_words)
g2_last_words.close()


g3 = open('manyworded_entries/manyword_entries_g3','wb')
pickle.dump(group3,g3)
g3.close()

g3_layer_2 = open('manyworded_entries/manyword_entries_g3_layer_2','wb')
pickle.dump(group3_second_layer,g3_layer_2)
g3_layer_2.close()

g4 = open('manyworded_entries/manyword_entries_g4','wb')
pickle.dump(group4,g4)
g4.close()

g4_last_words = open('manyworded_entries/manyword_entries_g4_last_words','wb')
pickle.dump(group4_last_words,g4_last_words)
g4_last_words.close()

print("ok, done lol")

# We're seeing two-worded verb-noun pairs, left-branching stemmer pairs (--> some of these have more than one word and should be put into group 4), manyformed entries ( , / )  and whole idioms,

# for group one, common words are : olla, saada, puhua, soittaa , ottaaa
# you probably want to clean the entries  - take away their exclamations and stuff.
# 'no' should make it go to group 4 ; 'ei' should put it in group 4 (or 3), or 'voi' ,or 'se' . . . maybe look into conjugations with -inen , iso and pieni . . .