import re
import pickle
file = open("sanalista/kotus-sanalista_v1.xml","rt",encoding="utf-8")

refined_corpus = set()

for line in file:
    match = re.search("<s>.*<\/s>",line)
    if match != None:
        match = match.group()
        match = re.sub("<(\/)?s>","",match)
        refined_corpus.add(match)
        print(match)
    else:
        print("This line gave NONE as a return value: %s"%line)

pickle_out = open("minun_sanalista","wb")
pickle.dump(refined_corpus,pickle_out)
pickle_out.close()