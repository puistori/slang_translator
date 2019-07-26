""" This file represents the main core of the library. It has the scripts required to
lemmatize words. It uses functions found in the return_forms.py file to do so. This is sort of 
the higher-level control point in the whole operation. 

""" 


from return_forms import *
from regex_dict import *

def lemmatize_nominal(word):
    end_list = []
    processing_list = []
    plurals_allowed = True
    word = word.lower()
    # Sometimes a word may look like it has a noun stem when it really has no such thing. For example, the verb
    # tutkii may look like the stem for a kaunis nominal, which would be lemmatized as tutkis. But in order for
    # that to be possible, the stem would have had to show up with another affix on it (like tutkiissa)
    # which it did not. This boolean keeps track of that.
    look_for_stem = False

    #sometimes, you want the original word without any endings clipped off - take the word poliisi for example.
    # the algorithm will think that the -si is a posessive ending, when it is not.
    # with the processing list, this mechanic should be unnecessary

    # step 1, remove ko marker
    # print(word)
    for index in range(len(questions)):
        boolean, result = ends_in(word, questions[index])
        boolean_2, result_2 = ends_in(word,false_questions[index])
        if boolean and not boolean_2:
            word = result
            break
        else:
            pass
    #Sometimes, words are just perfect the way they are, lol.
    end_list += return_passives(word)
    end_list += return_past_participles(word)
    print(end_list)
    if confusable_noun_ending_dict.refer(word):
        end_list.append(word)


    # step 2, remove posessive:
    for pos in possesives:
        boolean, result = ends_in(word, pos)
        if boolean:
            look_for_stem = True
            word = result
            ### Stem change time!
            if word[len(word) - 1] == "e" and word[len(word) - 2:] != "ee":
                word = word[0:len(word) - 1] + 'i'
            else:
                pass

            break
        else:
            pass

    # step 3, look for partitive endings. Return all possibilities.
    # At this point, stuff might start forking out.
    processing_list.append(word)
    mediating_list = []
    mediating_list = return_partitive_plurals(word)
    if len(mediating_list)> 0:
        look_for_stem = True
        processing_list+= mediating_list

    mediating_list += return_partitive_singulars(word)
    if len(mediating_list)> 0:
        look_for_stem = True
        processing_list+= mediating_list
    processing_list = remove_copies(processing_list)
    # step 4, remove locatives:
    # to be honest, you should only check for a hard_loc on the original word
    mediating_list += return_hard_loc(word)
    if len(mediating_list)> 0:
        look_for_stem = True
        processing_list+= mediating_list
    if word[len(word)-1] in ["n","t"]:
        plurals_allowed = False
    # check for soft locative:
    mediating_list += return_soft_loc(word)
    if len(mediating_list)> 0:
        look_for_stem = True
        processing_list+= mediating_list
    # this fix might be a little too barbaric... I'm trying to make it so that the original word gets kicked out
    # if we find out that it has a case ending on it. That way we don't return TOO many superflous options along
    # with the right answer.

    # Now checking it out for plural genetives
    mediating_list += return_plural_genetive(word)
    if len(mediating_list) > 0:
        look_for_stem = True
        plurals_allowed = True
        processing_list += mediating_list
    """
    # You shouldn't need this after the advent of the processing list
    if len(end_list) > 1 and keep_original == False:
        end_list = [a for a in end_list if a != word]
    """
    # now it's time to check for superlatives and instrumentals .. e.g. in ones.
    mediating_list = []
    kick_me_out = []
    for stem_candidate in processing_list:
        boolean,response = return_superlatives_or_instrumentals(stem_candidate)
        if boolean:
            kick_me_out.append(stem_candidate)
            end_list += response
    processing_list = [a for a in processing_list if a not in kick_me_out]
    processing_list = remove_copies(processing_list)
    # now it's time to check for comparatives.

    for stem_candidate in processing_list:
        mediating_list = return_comparatives(stem_candidate)
        if len(mediating_list) > 0:
            look_for_stem = True
            processing_list += mediating_list
    # Ok, these are all the possible stems. Now what we need to do, is turn these possible stems into lexical roots.

    if look_for_stem:
        # switching hands here
        substitute_processing_list = processing_list
        processing_list = []
        #print("sub")
        #print(substitute_processing_list)
        for stem in substitute_processing_list:
            add_stem = True
            ongoing_list = []
            #print(plurals_allowed)
            ongoing_list += nominal_stem_to_lemma(stem,plurals_allowed)[1]
            #print("stem to lemma %s"%ongoing_list)
            ongoing_list += post_processing(stem)
            #print("post processin %s "%ongoing_list)
            # A stem that we find, like tullut, has no chance of also being the right answer by itself,
            # so we don't need to add in the original.
            past_participles_returned = return_past_participles(stem)
            if len(past_participles_returned) > 0:
                add_stem = False
            ongoing_list += past_participles_returned
            #print("pass participles %s" % ongoing_list)
            ongoing_list += return_past_passive_participles(stem)
            #print("passs passive %s" %ongoing_list)
            if add_stem:
                ongoing_list.append(stem)
            end_list += ongoing_list
    end_list.append(word)
    end_list = remove_copies(end_list)

    return (end_list)


verbal_endings = ["mme", "tte", "vat", "vät", "n", "t"]


def lemmatize_verb(word):
    end_list = []
    test_list = []
    word = word.lower()
    possibilities = []
    # step 1, remove ko marker
    # print(word)
    for marker in questions:
        boolean, result = ends_in(word, marker)
        if boolean:
            word = result
            break
        else:
            pass

    # This is to see if the word is a verb in the first infinitive.
    if verb_ending_dict.refer(word):
        end_list.append(word)

    # This is to check off that the word could indeed be a conjugated verb, and clears it for verb-stem-analysis
    # Ehh, maybe it's better to nullify this feature.
    possibilities.append(word)
    conjugated_verb_boolean = False

    for ending in verbal_endings:
        boolean, result = ends_in(word, ending)
        if boolean:
            conjugated_verb_boolean = True
            if ending not in ["vat","vät"]:
                boolean, mandatory,original,changed = consonant_gradation_harden(result)
                if boolean:
                    word = changed
                    possibilities.append(word)
                    if not mandatory:
                        possibilities.append(original)
                else:
                    word = original
                    possibilities.append(word)
            else:
                word = result
                possibilities.append(word)
            break

            # this is for the +V personal ending seen in the third person singular present, e.g. puhuU
    if  conjugated_verb_boolean == False:
        if word[len(word)-2] in vowels and word[len(word)-1] == word[len(word)-2]:
            conjugated_verb_boolean = True
            possibilities.append(word)
        # or, it could be a past tense verb in the third person singular, like 'tiedotti'
        elif word[len(word)-1] == 'i':
            possibilities.append(word)

    # Check for passive forms.
    mediating_list = return_passives(word)
    if len(mediating_list) > 0:
        end_list += mediating_list
        conjugated_verb_boolean = True

    # So, I have ths for loop here because it's logically possible that there is an ambiguity related to
    # consonant gradation. Imagine a word like Haavia, found in this form: haavin . It coulda been haapia or haavia,
    # who would know?
    for option in possibilities:
        possible_option = option
        # Check for a conditional ending!
        boolean, result = ends_in(possible_option, "isi")
        if boolean:
            conjugated_verb_boolean = True
            possible_option = result
            test_list.append(possible_option)
            # If you see a verb declined with the conditional, it's ambiguous with respect to it's declension.
            # It could be a Saada verb, or a huomata verb, or an antaa verb.
            # Also, you need to take into account whether the verb is a verb like Tulla or Nousta. I'm operationalizing it
            # thusly : IF the last letter, after removing the the 'isi' is a consonant, then it belongs to one of those
            # classes, and I should add an e so that the rest of the program can correctly identify it
            # (e.g. tulisivat - isivat = tul , tule will get picked up correctly.

            if possible_option[len(possible_option) - 1] not in vowels:
                test_list.append(possible_option + "e")
            else:
                test_list.append(possible_option + "a")
                test_list = correct_for_harmony(test_list, "a")

        else:
            boolean,mediating_list = past_tense_verb_stem_to_lemma(possible_option)

            if boolean:
                end_list += mediating_list
                conjugated_verb_boolean = True
            else:
                test_list.append(possible_option)
        # This used to be "If conjugated_verb_boolean" but then negative forms of words like  "pysty"
        #  for "ei pysty" didn't float through. It might be worth it to just widen the net, so to speak.
        if True:
            mediating_list = []
            for wordie in test_list:
                mediating_list = verb_stem_to_lemma(wordie)
                end_list += mediating_list
        end_list = remove_copies(end_list)
    return (end_list)