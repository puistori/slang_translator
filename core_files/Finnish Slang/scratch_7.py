from lemmatizers import *
import re

# I think the last bastion is the present passive participles

corpus = open("sata_lasissa.txt","rt",encoding="utf-8")
string = ""
for line in corpus:
    string += line

master_list = []
#verbs in master list 2
master_list_2 = []
print(string)
string = re.sub("[,\.\(\)\"\!\n]","",string)



corpus = re.split(" ",string)

for word in corpus:
    mediating_list = list(lemmatize_nominal(word))
    mediating_list = remove_copies(mediating_list)
    mediating_list = tuple(mediating_list)
    master_list.append(mediating_list)
    mediating_list_2 = list(lemmatize_verb(word))
    mediating_list_2 = remove_copies(mediating_list_2)
    mediating_list_2 = tuple(mediating_list_2)
    master_list_2.append(mediating_list_2)

tuple_list = []

print(len(corpus))
print(len(master_list))

for index in range(len(corpus)):
    tuple_list.append( (corpus[index],master_list[index],master_list_2[index]) )

for input,output_noun,output_verb in tuple_list:
    print ("%s    Noun: %s      Verb:  %s"%(input,output_noun,output_verb))


print(lemmatize_verb("epäilee"))