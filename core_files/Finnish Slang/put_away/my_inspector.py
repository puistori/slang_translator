import pickle


our_dict = pickle.load(open("found_slang_words","rb"))
for key in our_dict:
    print("%s : %s"%(key,our_dict[key][0]))
    print("Example : %s"%(our_dict[key][1]))

our_failed_searches = pickle.load(open("failed_searches","rb"))

for element in our_failed_searches:
    print(element)

our_impropers = pickle.load(open("probably_improper_word_forms","rb"))

for element in our_impropers:
    print(element)


if "byygeen" in our_impropers:
    print("yayeuh")