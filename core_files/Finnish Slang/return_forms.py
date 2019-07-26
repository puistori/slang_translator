from basic_word_manipulation import *
from regex_dict import *
def return_partitive_plurals(word):
    end_list = []
    p_p_e_found = False
    for p_p_e in partitive_plural_map:
        temp_word = ""
        boolean, result = ends_in(word,p_p_e)
        if boolean:
            p_p_e_found = True
            for p_p_e_possibility in partitive_plural_map[p_p_e]:
                temp_word = result + p_p_e_possibility
                end_list.append(temp_word)
            break
    if p_p_e_found == False:
        pass
    return end_list


### Might need to deal with ta partitives... like Oikeata
def return_partitive_singulars(word):
    end_list = []
    p_s_e_found = False
    for p_s_e in partitive_singular_map:
        temp_word = ""
        boolean, result = ends_in(word,p_s_e)
        if boolean:
            p_s_e_found = True
            for p_s_e_possibility in partitive_singular_map[p_s_e]:
                temp_word = result + p_s_e_possibility
                end_list.append(temp_word)
    if p_s_e_found == False:
        # Now we gotta handle partitives made by the Vowel + A()
        boolean,result = ends_in(word,"a")
        if boolean and word[len(word)-2] in vowels:
            end_list.append(word[:len(word)-1])
        else:
            boolean,result = ends_in(word,"ä")
            if boolean and word[len(word) - 2] in vowels:
                end_list.append(word[:len(word) - 1])
    end_list = remove_copies(end_list)
    return end_list

def return_comparatives(word):
    end_list = []
    for comp_ending in comparatives:
        boolean, result = ends_in(word, comp_ending)
        if boolean:
            boolean,mandatory, original, changed = consonant_gradation_harden(result)
            # this is the point where I discard the option of the -mpi being a mere coincidence.
            candidate = original
            end_list.append(original)
            if boolean:
                end_list.append(changed)
            break
    return (end_list)
""""
# This is getting replaced by a version of the function that uses a regex dict.
def return_hard_loc(word):
    end_list= []
    for hard_loc in hard_locatives:
        boolean, result = ends_in(word, hard_loc)
        if boolean:
            #get_rid_of_these.append(word)
            word = result
            ### Stem change time!
            boolean, mandatory, original, changed = consonant_gradation_harden(word)
            # If you uncomment this line, then you will also return the non-changed version no matter what
            #end_list.append(original)
            if boolean:
                end_list.append(changed)
                if not mandatory:
                    end_list.append(original)
            else:
                end_list.append(original)

            # maybe, just maybe, there is a "vanishing k"
            if word[len(word) - 1] in vowels and word[len(word) - 2] in vowels:
                vanishing_k_version = word[0:len(word) - 1] + "k" + word[len(word) - 1]
                end_list.append(vanishing_k_version)
            break
        else:
            pass
    return(end_list)
"""

"""
# Ok, so the word might belong to an 'e' declension, in which case you would need to soften it, rather
        # than harden it.. think of words like koe
        boolean,result = ends_in(clipped_word,"ee")
        if boolean:
            original,changed = consonant_gradation_soften(clipped_word)
            if changed != "":
                end_list.append(changed)
            else:
                end_list.append(original)
        else:
            boolean,result = ends_in(clipped_word,"ei")
            if boolean:
                original, changed = consonant_gradation_soften(clipped_word)
                if changed != "":
                    end_list.append(changed)
                else:
                    end_list.append(original)
            else:
            """

def return_hard_loc(word):
    end_list= []
    result = hard_locatives_dict.refer_to_function(word)
    if result != False:
        clipped_word = word[:len(word)-result]
        #we don't want to do any consonant gradation if the stem belongs to an 'e' class of words though,
        # like koe.
        not_an_e_stem = True
        if clipped_word[len(clipped_word)-2:] in ["ee","ei"]:
            not_an_e_stem = False
        boolean,mandatory,original,changed = consonant_gradation_harden(clipped_word)
        if boolean and mandatory and not_an_e_stem:
            end_list.append(changed)
        elif boolean and not_an_e_stem:
            end_list.append(changed)
            end_list.append(original)
        else:
            end_list.append(original)
        # maybe, just maybe, there is a "vanishing k"
        if word[len(word) - 1] in vowels and word[len(word) - 2] in vowels:
            vanishing_k_version = word[0:len(word) - 1] + "k" + word[len(word) - 1]
            end_list.append(vanishing_k_version)
        else:
            pass

    return(end_list)


"""
def return_soft_loc(word):
    end_list = []
    for soft_loc in soft_locatives:
        boolean, result = ends_in(word, soft_loc)
        if boolean:
            if soft_loc in ["na","nä"]:
                end_list.append(result)
                break
            elif soft_loc == "eeseen":
                end_list.append(result+soft_loc[:2])
            else:
                word = result + soft_loc[0]
                end_list.append(word)
                break
        else:
            pass
    return(end_list)
"""


def return_soft_loc(word):
    end_list = []
    result = soft_locatives_dict.refer(word)
    if result != False:
        match = soft_locatives_dict.return_match(word)
        boolean,stem = ends_in(word,match)
        answer = stem
        if result > 0:
            add_on = match[:result]
            answer += add_on
        return ([answer])
    else:
        return([])

    return(end_list)


"""
def return_superlatives_or_instrumentals(word):
    end_list = []
    boolean,result = ends_in(word,"in")
    if boolean:
        if result[len(result)-1] not in vowels:
            mediating_list = [result+"i"]
            if detect_harmony(mediating_list[0]) == True:
                mediating_list += [result+"ä"]
            elif detect_harmony(mediating_list[0])== False:
                mediating_list += [result+"a"]
            else:
                mediating_list += [result +"a"]
                mediating_list += [result + "ä"]
        else:
            mediating_list = [result]
        for stem_candidate in mediating_list:
            boolean,mandatory,original,changed = consonant_gradation_harden(stem_candidate)
            end_list.append(original)
            if boolean:
                end_list.append(changed)
    remove_copies(end_list)
    return(end_list)
"""

# revamped version

def return_superlatives_or_instrumentals(word):
    end_list = []
    for superlative_ending in superlative_endings:
        boolean,result = ends_in(word,superlative_ending)
        if boolean:
            boolean_2,answer = plural_nominal_stem_to_lemma(result)
            if boolean_2:
                for candidate in answer:
                    boolean,mandatory, original,changed = consonant_gradation_harden(candidate)
                    if boolean and mandatory:
                        end_list.append(changed)
                    elif boolean:
                        end_list.append(original)
                        end_list.append(changed)
                    else:
                        end_list.append(original)
                return(True,end_list)
    return(False,[])



def return_past_passive_participles(word):
    # this returns lemmas, not stems.
    end_list = []
    past_passive_participle_endings = {"ettu": [(-4, "aa")], "ttu": [(-2, "a"), (-3, "a")], "ntu": [(-2, "na")],
                                       "ltu": [(-2, "la")], \
                                       "stu": [(-1, "a")], "tu": [(-2, "da")], "etty": [(-4, "ää")],
                                       "tty": [(-2, "ä"), (-3, "ä")], \
                                       "nty": [(-2, "nä")], "lty": [(-2, "lä")], \
                                       "sty": [(-1, "ä")], "ty": [(-2, "dä")]}

    for past_passive_participle_ending in past_passive_participle_endings:
        boolean, result = ends_in(word, past_passive_participle_ending)
        if boolean:
            for solution in past_passive_participle_endings[past_passive_participle_ending]:
                # This conditional statement is needed because some of the patterns will need special treatment
                # with respect to consonant gradation.
                if past_passive_participle_ending in ["ettu", "etty"] or \
                        (past_passive_participle_ending in ["ttu", "tty"] and solution[0] == -3):
                    word = word[:len(word) + solution[0]] + solution[1]
                    #print("printing de word")
                    #print(word)
                    boolean,mandatory,original, changed = consonant_gradation_harden(word)
                    if boolean:
                        word = changed
                    # I commented this out and added a +solution[1] when word is getting redefined up there...
                    #This made it all work with words like annettu
                    #word += solution[1]
                    end_list.append(word)

                else:
                    word = word[:len(word) + solution[0]] + solution[1]
                    end_list.append(word)
            break
    return(end_list)

def return_passives(word):
    # these are kinda ambiguous TBH just sayin lol
    # unlikely TBH. ..
    # at any rate, this thing will return the lemma on past passives, and present passives.
    end_list = []
    present_passive_endings = ["etaan","taan","nnaan","llaan","staan","daan",\
                               "etään","tään","nnään","llään","stään","dään"]

    for present_passive_ending in present_passive_endings:
        boolean,result = ends_in(word,present_passive_ending)
        if boolean:
            # This conditional statement is needed because some of the patterns will need special treatment
            # with respect to consonant gradation.
            if present_passive_ending == "etaan":
                word = result + "aa"
                boolean,mandatory,original,changed = consonant_gradation_harden(word)
                if boolean:
                    word = changed
            elif present_passive_ending == "etään":
                word = result + "ää"
                boolean, mandatory, original, changed = consonant_gradation_harden(word)
                if boolean:
                    word = changed
                end_list.append(word)
            else:
                end_list.append(word[:len(word)-2])
                if present_passive_ending == "taan":
                    end_list.append(word[:len(word)-4]+"a")
                elif present_passive_ending == "tään":
                    end_list.append(word[:len(word) - 4] + "ä")

    past_passive_endings = {"ettiin":[(-6,"aa")],"ttiin":[(-4,"a"),(-5,"a")],"ntiin":[(-4,"na")],"ltiin":[(-4,"la")],\
                            "stiin":[(-3,"a")],"tiin":[(-4,"da")]}

    for past_passive_ending in past_passive_endings:
        boolean,result = ends_in(word,past_passive_ending)
        if boolean:
            for solution in past_passive_endings[past_passive_ending]:
                # This conditional statement is needed because some of the patterns will need special treatment
                # with respect to consonant gradation.
                if past_passive_ending == "ettiin" or (past_passive_ending == "ttiin" and solution[0] == -5):
                    word = word[:len(word)+solution[0]]
                    boolean, mandatory, original,changed = consonant_gradation_harden(word)
                    if boolean:
                        word = changed
                    word += solution[1]
                    end_list.append(word)
                    end_list = correct_for_harmony(end_list,solution[1])

                else:
                    word = word[:len(word)+solution[0]] + solution[1]
                    end_list.append(word)
                    end_list = correct_for_harmony(end_list, solution[1])
            break


    conditional_passive_endings = {"ettaisiin":[(-9,"aa")],"ttaisiin":[(-7,"a"),(-8,"a")],"ntaisiin":[(-7,"na")],"ltaisiin":[(-7,"la")],\
                            "staisiin":[(-5,"")],"taisiin":[(-7,"da")],"ettäisiin":[(-9,"ää")],"ttäisiin":[(-7,"ä"),(-8,"ä")],\
                                       "ntäisiin":[(-7,"nä")],"ltäisiin":[(-7,"lä")],\
                            "stäisiin":[(-5,"ä")],"täisiin":[(-7,"dä")]}

    for conditional_passive_ending in conditional_passive_endings:
        boolean, result = ends_in(word, conditional_passive_ending)
        if boolean:
            for solution in conditional_passive_endings[conditional_passive_ending]:
                # This conditional statement is needed because some of the patterns will need special treatment
                # with respect to consonant gradation.
                if conditional_passive_ending in ["ettaisiin","ettäisiin"] or \
                        (conditional_passive_ending in ["ttaisiin","ttäisiin"] and solution[0] == -8):
                    word = word[:len(word) + solution[0]]
                    boolean, mandatory, original, changed = consonant_gradation_harden(word)
                    if boolean:
                        word = changed
                    word += solution[1]
                    end_list.append(word)

                else:
                    word = word[:len(word) + solution[0]] + solution[1]
                    end_list.append(word)
            break
    return(end_list)

def return_past_participles(word):
    end_list = []
    # i had to add some to account for colloquial endings.
    nut_case_endings = {"llee": (-2, "a"), "ssee": (-3, "ta"), "nnee": (-4, "ta"), "nee": (-3, "a"),\
                        "nnut": (-4, "ta"), "nnyt": (-4, "tä"), "nut": (-3, "a"), "nyt": (-3, "ä"), \
                        "ssut": (-3, "ta"), "ssyt": (-3, "tä"), "llut": (-2, "a"), "llyt": (-2, "ä"), \
                        "nnu": (-3, "ta"), "nny": (-3, "tä"), "nu": (-2, "a"), "ny": (-2, "ä"), \
                        "ssu": (-2, "ta"), "ssy": (-2, "tä"), "llu": (-1, "a"), "lly": (-1, "ä")}
    for nut_case_ending in nut_case_endings:
        boolean, result = ends_in(word, nut_case_ending)
        if boolean:
            # Now we have to deal with saada type verbs. The way I'll operationalize it, is that if the stem has
            # two vowels, it's a saada verb.
            if (nut_case_ending == "nut" or nut_case_ending == "nu") and len(result)>2 and (result[len(result)-1] in vowels or result[len(result)-1] == 'h')\
                and result[len(result)-2] in vowels:
                end_list.append(result+"da")
            elif (nut_case_ending == "nyt" or nut_case_ending == "ny") and len(result) > 2 and (
                    result[len(result) - 1] in vowels or result[len(result) - 1] == 'h') \
                    and result[len(result) - 2] in vowels:
                end_list.append(result + "dä")
            else:
                lisättävä_sana = word[:len(word) + nut_case_endings[nut_case_ending][0]] + \
                                 nut_case_endings[nut_case_ending][1]
                end_list.append(lisättävä_sana)
                end_list = correct_for_harmony(end_list, nut_case_endings[nut_case_ending][1])
                if nut_case_ending in ["nnee", "nnut", "nnyt"]:
                    lisättävä_sana = word[:len(word) - 2] + "a"
                    end_list.append(lisättävä_sana)
                    # If you want, you could add a third, optional argument that specifies a target that you are
                    # looking for
                    end_list = correct_for_harmony(end_list, "a")
                break
    end_list = remove_copies(end_list)
    return(end_list)


def post_processing(word):
    # The purpose of this function is to take words in forms like the fourth infinitive and then return them
    # to their stems.
    end_list = []
    mediating_list = []
    # I'm calling these clippable endings because the stem of the word that has them can be found
    # by just clipping them off.
    clippable_endings = ["minen","ma","mä","va","vä"]
    for clippable_ending in clippable_endings:
        boolean,result = ends_in(word,clippable_ending)
        if boolean:
            mediating_list.append(result)
            break

    # Now that you've found the verb stems, go ahead and turn them into lemmas!

    mediating_list = remove_copies(mediating_list)
    for element in mediating_list:
        root = verb_stem_to_lemma(element)
        end_list += root

    # return the lemmas!
    return (end_list)


def verb_stem_to_lemma(word):
    end_list = []
    boolean, result = ends_in(word, "ee")
    if boolean:
        boolean, result = ends_in(word, "e")
        word = result
    # Tarvita verbs
    if len(word) > 4 and word[len(word) - 4:] == "itse":
        boolean, result = ends_in(word, "se")
        if detect_harmony(word) == True:
            word = result + "ä"
            end_list.append(word)
        elif detect_harmony(word) == False:
            word = result + "a"
            end_list.append(word)
        else:
            end_list.append(result + "a")
            end_list.append(result + "ä")
    # Lämmetä verbs
    elif len(word) > 2 and word[len(word) - 2:] == "ne":
        boolean, result = ends_in(word, "ne")
        original, changed = consonant_gradation_soften(result)

        if changed != "":
            word = changed
        else:
            word = original

        if detect_harmony(word) == True:
            word = word + "tä"
            end_list.append(word)
        elif detect_harmony(word) == False:
            word = word + "ta"
            end_list.append(word)
        else:
            end_list.append(word + "ta")
            end_list.append(word + "tä")
    # Nousta verbs
    elif len(word) > 2 and word[len(word) - 2:] == "se":
        boolean, result = ends_in(word, "e")
        if detect_harmony(word) == True:
            word = result + "tä"
            end_list.append(word)
        elif detect_harmony(word) == False:
            word = result + "ta"
            end_list.append(word)
        else:
            end_list.append(result + "ta")
            end_list.append(result + "tä")
    # Tulla verbs
    elif len(word) > 2 and word[len(word) - 2:] == "le":
        # remember, this causes consonant gradation :O
        boolean,result = ends_in(word,"le")
        original,changed = consonant_gradation_soften(result)
        if changed != "":
            to_be_added = changed
        else:
            to_be_added = original
        to_be_added += "le"
        boolean, result = ends_in(to_be_added, "e")
        if detect_harmony(word) == True:
            word = result + "lä"
            end_list.append(word)
        elif detect_harmony(word) == False:
            word = result + "la"
            end_list.append(word)
        else:
            end_list.append(result + "la")
            end_list.append(result + "lä")

    # antaa verbs, if it's not the third person singular (cv is what we'll be left with)

    elif word[len(word) - 1] in vowels and word[len(word) - 2] not in vowels:
        mediating_list = []
        if detect_harmony(word) == True:
            word += "ä"
            mediating_list.append(word)
        elif detect_harmony(word) == False:
            word += "a"
            mediating_list.append(word)
        else:
            mediating_list.append(word + "a")
            mediating_list.append(word + "ä")
        for word in mediating_list:
            boolean, mandatory,original, changed = consonant_gradation_harden(word)
            end_list.append(original)
            if boolean:
                end_list.append(changed)

    # This next elif statement is here to detect Vta verbs that have vowels other than a/ä  as their V, and which
    # are inflected to the third person singular... In other words, verbs like "haluaa" with three vowels in a row.
    elif word[len(word)-1] in ["a","ä"] and word[len(word)-2] in ["a","ä"] and word[len(word)-3] in vowels:
        original,changed = consonant_gradation_soften(word[:len(word)-2])
        if changed != "":
            answer = changed +"ta"
            answer = [answer]
            answer = correct_for_harmony(answer,"ta")
            end_list += answer
        else:
            answer = original + "ta"
            answer = [answer]
            answer = correct_for_harmony(answer, "ta")
            end_list += answer
    # either huomata verbs, saada verbs, or antaa verbs in the third person singular. There is no apriori way of knowing.
    # WEll, one thing you can do to disambiguate, is see if the second vowel is an a. If it's not, it can't be a V-TA verb
    # All possibilities will be returned. The assumption is that there is no magic K.
    elif word[len(word) - 1] in vowels and word[len(word) - 2] in vowels:
        # It could be a word like Varata, for all we know. Let's be sure.
        if word[len(word)-1] in ["a","ä"] and word[len(word)-2] in ["a","ä"]:
            ata_verb, changed = consonant_gradation_soften(word)
            if changed != "":
                ata_verb = changed
            ata_verb = ata_verb[:len(word)-2]
            ata_verb += "ta"
            ata_verb = [ata_verb]
            ata_verb = correct_for_harmony(ata_verb,"ta")
            end_list += ata_verb
        # It could also be a regular old Antaa verb.
        antaa_verb = [word[:len(word)-1] +"a"]
        antaa_verb = correct_for_harmony(antaa_verb,"a")
        end_list += antaa_verb
        # It could also be a Saada verb
        saada_verb = [word+"da"]
        saada_verb = correct_for_harmony(saada_verb,"da")
        end_list+= saada_verb
    end_list = remove_copies(end_list)
    return(end_list)


def nominal_stem_to_lemma(word,plurals_allowed=True):
    end_list = []
    has_special_stem = False
    has_a_double = False
    for double_stem in stem_dictionary_doubles:
        consonant_gradation = False
        if double_stem in ["aa", "ai", "ei", "ii","ee"]:
            consonant_gradation = True
        boolean, result = ends_in(word, double_stem)
        if boolean:
            has_a_double = True
            has_special_stem = True

            if consonant_gradation:
                original,changed = consonant_gradation_soften(word)
                if changed != "":
                    boolean,result = ends_in(changed,double_stem)
            for possibility in stem_dictionary_doubles[double_stem]:
                possible_answer = result + possibility
                if plurals_allowed == False and double_stem in plural_double_stems_list:
                    pass
                else:
                    end_list.append(possible_answer)
    if has_a_double == False:
        for single_stem in stem_dictionary_singles:
            boolean, result = ends_in(word, single_stem)
            if boolean:
                has_special_stem = True
                for possibility in stem_dictionary_singles[single_stem]:
                    if plurals_allowed == False and possibility == "a" and single_stem == "i":
                        pass
                    else:
                        possible_answer = result + possibility
                        possible_answer = correct_for_harmony([possible_answer],possibility)
                        for element in possible_answer:
                            end_list.append(element)

                # Ok, now to correct for harmony.
                # Is this outdated? should I fix this? It seems to work just fine, but it is a little clunky-looking
                mediating_list = []
                for final_stem_candidate in end_list:
                    #print("this was a candidate: %s" % final_stem_candidate)
                    if detect_harmony(final_stem_candidate) and \
                            final_stem_candidate[len(final_stem_candidate) - 1] == "a":
                        new_final_candidate = final_stem_candidate[0:len(final_stem_candidate) - 1] + "ä"
                        mediating_list.append(new_final_candidate)
                    elif detect_harmony(final_stem_candidate) == None and \
                            final_stem_candidate[len(final_stem_candidate) - 1] == "a":
                        mediating_list.append(final_stem_candidate)
                        new_final_candidate = final_stem_candidate[0:len(final_stem_candidate) - 1] + "ä"
                        mediating_list.append(new_final_candidate)
                    else:
                        mediating_list.append(final_stem_candidate)
                        #print("adding to the mediating list: %s" % final_stem_candidate)
                actual_end_list = mediating_list

    return (has_special_stem,end_list)


def past_tense_verb_stem_to_lemma(word):
    end_list = []
    end_boolean = False
    boolean, result = ends_in(word, "i")
    if boolean:
        # check if it's a huomata verb
        boolean, result = ends_in(word, "si")
        # ok, potentially, a verb like "Toisia" might fall under this , so it could be good to clone.
        # Oh , yeah, and Nousta verbs will get stuck in here too lol
        # it IS unlikely tho. # maybe add an "unlikely" tag via a dictionary?
        if boolean == True and result[len(result) - 1] in vowels:
            mediating_list_2 = []
            mediating_list_3 = []
            mediating_list_4 = []
            mediating_list_2.append(word + "a")
            mediating_list_2= correct_for_harmony(mediating_list_2, "a")
            mediating_list_3.append(result + "ta")
            mediating_list_3 = correct_for_harmony(mediating_list_3, "ta")
            mediating_list_4.append(word[:len(word)-1]+"ta")
            mediating_list_4 = correct_for_harmony(mediating_list_4,"ta")
            end_list += mediating_list_2
            end_list += mediating_list_3
            end_list += mediating_list_4
            end_boolean = True
        # Now, rakentaa verbs!!
        elif boolean and result[len(result) - 1] == "n":
            end_list.append(result + "taa")
            end_list = correct_for_harmony(end_list, "taa")
            end_boolean = True
        # now to see if it is a tulla, tarvita or lämmetä verb. I am creating two different options here
        # because it is theoretically speaking possible hat a verb like vaalimme could be vaalia or vaalla
        elif word[len(word) - 2] in ["l", "n"]:
            # the other option will get picked up on later. It should now look like a present tense tulla stem or whatever
            other_option = word[:len(word) - 1] + "e"
            other_option = verb_stem_to_lemma(other_option)
            # This below here said test_list.append, wasn't really sure what to say about that lol
            end_list += (other_option)
            end_list.append(word + "a")
            end_list = correct_for_harmony(end_list, "a")
            end_boolean = True

        # Now check if it's a saada verb or an antaa verb. At this point, there is some ambiguity because
        # a verb like antoivat COULD have been generated from any of the following : antooda, antoida, antaa, antoa.
        # maybe a likeliness thing would be good here too... although, I will go on a limb and say that ALL
        # saada verbs with polysyllabic stems are -oida verbs. That might help disambiguate actually
        else:
            # saada and luennoida verbs
            if count_syllables(word) == 1 and word[len(word) - 2] in vowels:
                end_list.append(word + "da")
                end_list.append(word[:len(word) - 1] + word[len(word)-1] + "da")
                end_list = correct_for_harmony(end_list, "da")
                end_boolean = True
            # luennoida verbs
            elif word[len(word) - 2] in ["o", "ö"]:
                end_list.append(word + "da")
                end_list = correct_for_harmony(end_list, "da")
                end_boolean = True
            # Now, antaa verbs :O Notice how it could satisfy both requirements, a verb
            # could logically be in either group.
            if word[len(word)-2] in vowels:
                #print(word)
                antaa_stems = word[:len(word) - 1] + "a"
                antaa_stems = correct_for_harmony([antaa_stems], "a")
                #print(antaa_stems)
                end_boolean = True
            else:
                antaa_stems = word[:len(word)] + "a"
                antaa_stems = correct_for_harmony([antaa_stems], "a")
                alternate_stem = word[:len(word)-1] + "aa"
                mediating_list = correct_for_harmony([alternate_stem],"aa")
                for mediating_candidate in mediating_list:
                    antaa_stems.append(mediating_candidate)
                end_boolean = True
            # ok this line I'll have to to do the old falshioned way
            if word[len(word) - 2] == "o":
                antaa_stems.append(word[:len(word) - 2] + "aa")
                end_boolean = True
            else:
                if detect_harmony(word) != False:
                    antaa_stems.append(word[:len(word) - 1] + "ää")
                    end_boolean = True


            for antaa_stem in antaa_stems:
                end_list.append(antaa_stem)

    return(end_boolean,end_list)

def return_plural_genetive(word):
    end_list = []
    solutions = plural_genetive_dict.refer(word)
    if solutions != False:
        for solution in solutions:
            boolean,answer = ends_in(word,solution[0])
            answer += solution[1]
            end_list.append(answer)
        return(end_list)
    else:
        return([])

# This function below here shouldn't actually be necessary, because the return past participles function can take
# words directly as stems and turn them into participles.
def return_inflected_nut_case_stem(word):
    boolean,result = ends_in(word,"nee")
    if boolean:
        answer = result+"nut"
        answer = correct_for_harmony([answer],"nut")
        return(answer)
    else:
        return([])




## this is the same thing as the nominal_stem_to_lemma function, except it ONLY works for plurals.
# this is intended to work in tandem with the instrumental / superlative function.
def plural_nominal_stem_to_lemma(word):
    end_list = []
    has_special_stem = False
    has_a_double = False
    for double_stem in plural_double_stems_list:
        consonant_gradation = False
        if double_stem in ["aa", "ai", "ei", "ii","ee"]:
            consonant_gradation = True
        boolean, result = ends_in(word, double_stem)
        if boolean:
            has_a_double = True
            has_special_stem = True
            if consonant_gradation:
                original,changed = consonant_gradation_soften(word)
                if changed != "":
                    boolean,result = ends_in(changed,double_stem)
            for possibility in stem_dictionary_doubles[double_stem]:
                possible_answer = result + possibility
                end_list.append(possible_answer)
    if has_a_double == False:
        boolean,result = ends_in(word,"i")
        #you have to exclude double i endings, kuz of like, past passives and stuff
        if boolean and result[len(result)-1] != "i":
            has_special_stem = True
            answer = [result+"a"]
            answer = correct_for_harmony(answer,"a")
            end_list+= answer
    return (has_special_stem,end_list)