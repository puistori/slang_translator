vowels =['a','ä','e','i','o','ö','u','y']
softened_list = ["p","t","k","v","d","mm","nn","ng","ll","rr"]
necessary_to_harden = ["p","t","k","ng"]
# hard locatives includes affixes near the root that cause consonant gradation. Most (but not all) of these are
# locatives, hence the name.
hard_locatives = ['ssa','ssä','lla','llä','lta','ltä','lle','sta','stä','n','t',"ksi","sti"]
soft_locatives = ['aan','ään','eeseen','een','iin','oon','öön','uun','yyn',"na","nä", \
                  'aansa', 'äänsä', 'eeseensä', 'eensä','eeseensa', 'eensa', 'iinsa',\
                  'iinsä', 'oonsa', 'öönsä', 'uunsa', 'yynsä']
possesives = ['ni','si','nsa','mme','nne']
questions = ['ko',"kö"]
false_questions = ['kko',"kkö"]
comparatives = ["mpi","mpa","mpä"]


softened_hash = {"p": "pp", "b": "bb", "t": "tt", "k": "kk", "g": "gg", "v": "p", "d": "t", "mm": "mp", "nn": "nt",
                 "ng": "nk", "ll": "lt", "rr": "rt"}
hardened_hash = {}
for key in softened_hash:
    hardened_hash[softened_hash[key]] = key
hardened_hash["k"] = ""



stem_dictionary_doubles ={"nee":["nut"],"aa":["as"],"ai":["as"],"ee":["e"],"ei":["e","is"],"ii":["is"],"oi":["a","o"],"ksi":["s"],\
                          "kse":["s"],"si":["nen","si"],"se":["nen"],"ttoma":["ton"],"ttömä":["tön"],"ttomi":["ton"],"ttömi":["tön"],\
                          "ui":["u"],"yi":["y"],"de":["si"]}

plural_double_stems_list = ["ai","ei","oi","ksi","si","ttomi","ttömi","ui","yi"]

plural_stem_dictionairy = {"ai":["as"],"ei":["e","is"],"oi":["a","o"],"ksi":["s"],"si":["nen","si"],"ttomi":["ton"], \
                           "ttömi": ["tön"],"ui":["u"],"yi":["y"],}

stem_dictionary_singles = {"e":["i"],"i":["i","a"]}


#partitive maps
partitive_plural_map = {"oja":["o","a"],"uja":["u"],"eja":["i"],"sia":["si","nen"],"siä":["si","nen"],"ia":["i","ia"],"iä":["i","iä"],\
                        "mia":["n","ma"],"miä":["n","mä"],"ai":["as"],"ita":[""],"itä":[""]}
# VA might be better to code in separately.
partitive_singular_map = {"lta":["l","lta"],"ltä":["l","ltä"],"nta":["ni","n"],"ntä":["ni","n"],"rta":["ri"],"rtä":["ri"],\
                          "sta":["nen","s","sta"],"stä":["nen","s","stä"],"utta":["us","ut"],"yttä":["ys","yt"],"että":["e"]}


superlative_endings = ["n","mpia","mpiä","mpa","mpä","mpien","mma","mmä"]


common_spoken_language_words = set(["etten","ettet","ettei","ettemme","ettette","et","en","mun","sun","ku","täl","viel",\
                                "vaik","oon","on","oo","ois","vaa","muutaki","nää","mä","sä","tä","tää",])



# the -as ones need to trigger softening. otherwise, you're good



# it's also worth remembering, that an e could also correspond to the front version of a
# that only happens with the singles,  I think though.
# that's probably easier to hardcode in later tho.