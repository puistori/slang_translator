import re
class regex_dict():
    def __init__(self):
        self.main_reference_table = {}
    def refer(self,input):
        for lookup in self.main_reference_table:
            if re.search(lookup,input):
                return(self.main_reference_table[lookup])
        return (False)

    def refer_to_function(self, input):
        for lookup in self.main_reference_table:
            if re.search(lookup,input):
                function = self.main_reference_table[lookup]
                partial_function = partial(function,lookup,input)
                answer = partial_function()
                return(answer)
        return (False)

    def return_match(self, input):
        for lookup in self.main_reference_table:
            if re.search(lookup,input):
                result = re.search(lookup,input)
                result = result.group()
                return(result)
        return (False)

    def add(self,key,reference):
        self.main_reference_table[key] = reference



verb_ending_dict = regex_dict()
verb_ending_dict.add(r"[aäeioöuy]st(a|ä)\b",True)
verb_ending_dict.add(r"[aäeioöuy]t(a|ä)\b",True)
verb_ending_dict.add(r"([aeiou]a|[äeiöy]]ä)\b",True)
verb_ending_dict.add(r"(lla|llä)\b",True)
verb_ending_dict.add(r"(nna|nnä)\b",True)
verb_ending_dict.add(r"(rra|rrä)\b",True)
verb_ending_dict.add(r"(da|dä)\b",True)


# i , nen, cvs, as,is, v(u/y)s, in, on - ön , el, hyt - ut (but there are so few!)
confusable_noun_ending_dict = regex_dict()
# these are noun-lemma endings that might get confused with something else in the parser.
# for example, the -n at the end of the common -nen diminuitive ending could be mistakenly seen
# as a genetive marker

confusable_noun_ending_dict.add(r"nen\b",True)
confusable_noun_ending_dict.add(r"in\b",True)
confusable_noun_ending_dict.add(r"t(o|ö)n\b",True)
confusable_noun_ending_dict.add(r"si\b",True)
confusable_noun_ending_dict.add(r"ni\b",True)


plural_genetive_dict = regex_dict()
plural_genetive_dict.add(r"iden\b",(("den",""),))
plural_genetive_dict.add(r"itten\b", (("tten",""),))
plural_genetive_dict.add(r"[oöuy]jen\b",(("jen","i"),))
plural_genetive_dict.add(r"sten\b",(("ten","e"),("ten","")))
plural_genetive_dict.add(r"nten\b",(("ten",""),("ten","i")))
plural_genetive_dict.add(r"rten\b",(("ten","i"),))
plural_genetive_dict.add(r"ien\b",(("en",""),))

hard_locatives = ['ssa','ssä','lla','llä','lta','ltä','lle','sta','stä','n','t',"ksi","sti"]

from functools import partial

def match_length(regEx,given_string):
    match = re.search(regEx,given_string)
    group = match.group()
    length = len(group)
    return(length)

#(partial(insert_phoneme,new_btn,self.target,self.clear_out))
# this is for the formal variety of the language.
hard_locatives_dict_formal = regex_dict()
hard_locatives_dict_formal.add(r"ss(a|ä)(\1n)?\b",match_length,)
hard_locatives_dict_formal.add(r"ll(a|ä)(\1n)?\b",match_length,)
hard_locatives_dict_formal.add(r"lt(a|ä)(\1n)?\b",match_length,)
hard_locatives_dict_formal.add(r"lle(en)?",match_length,)
hard_locatives_dict_formal.add(r"st(a|ä)(\1n)?\b",match_length,)
hard_locatives_dict_formal.add(r"n\b",match_length,)
hard_locatives_dict_formal.add(r"t\b",match_length,)
# I don't know, do they do the V+N possessive marker after ksi?
hard_locatives_dict_formal.add(r"ksi",match_length,)
hard_locatives_dict_formal.add(r"sti",match_length,)

#print(hard_locatives_dict.refer_to_function("ssa"))


hard_locatives_dict = regex_dict()
hard_locatives_dict.add(r"(?<=[aäeioöuy])s(s(a|ä)(\2n)?)?\b",match_length,)
hard_locatives_dict.add(r"(?<=[aäeioöuy])l(l(a|ä)(\2n)?)?\b",match_length,)
hard_locatives_dict.add(r"(?<=[aäeioöuy])l(t(a|ä)(\2n)?)?\b",match_length,)
hard_locatives_dict.add(r"lle(en)?",match_length,)
hard_locatives_dict.add(r"st((a|ä)(\2n)?)?\b",match_length,)
hard_locatives_dict.add(r"n\b",match_length,)
hard_locatives_dict.add(r"t\b",match_length,)
# I don't know, do they do the V+N possessive marker after ksi?
hard_locatives_dict.add(r"ks(i)?\b",match_length,)
hard_locatives_dict.add(r"sti\b",match_length,)



soft_locatives = ['aan','ään','eeseen','een','iin','oon','öön','uun','yyn',"na","nä", \
                  'aansa', 'äänsä', 'eeseensä', 'eensä','eeseensa', 'eensa', 'iinsa',\
                  'iinsä', 'oonsa', 'öönsä', 'uunsa', 'yynsä']

soft_locatives_dict = regex_dict()
soft_locatives_dict.add(r"n(a|ä)",0)
soft_locatives_dict.add(r"(?<!ees)([aeiou])\1((n)(sa)?)?\b",1)
soft_locatives_dict.add(r"(?<!ees)([äeiöy])\1((n)(sä)?)?\b",1)
soft_locatives_dict.add(r"eeseen",2)
soft_locatives_dict.add(r"[aäeioöuy]ihin(s(a|ä))?",1)

