"""
1
I'm scratching my head about whether I should make posessive pronoun removal optional or not. If I make it mandatory,
a word like poliisi will get misparsed, however I think that that may be a rare phenomenon.

2
avain nominals


3
not sure what to do about making "d" a necessary to harden. I took it off, so that the system could return a word like
uudessa as uude, and maybe then pick that stem up as an si word.

4
for some reason, in the nominal_stem_to_lemma thing, I had stems ending in a single e map on to words ending with an a.
for the life of me, I can't figure out why I did this.

 in the nominal_stem_to_lemma thing, I had to change up the last part of code where it starts talking about turning
stems into lemmas. Part of the problem, is the nominal_stem_to_lemma() function can return two types of data - data
that is in need of further downstream processing (like nut case words) and data that is not (most everything else).
If you unnecessarily float things through downstream processing, you get too many extra answers. So, I decided to
have nut case stems get identified by a separate function. the old code is here:



 mediating_list_2 = []
        mediating_list_3 = []
        substitute_end_list = end_list
        print("der substitute : %s"%substitute_end_list)
        end_list = []
        for stem_candidate in substitute_end_list:
            boolean, mediating_list = nominal_stem_to_lemma(stem_candidate)
            if boolean:
                mediating_list_2 += mediating_list
                #mediating_list_3.append(stem_candidate)
            else:
                mediating_list_2.append(stem_candidate)
        end_list += mediating_list_2
    # this will make it so we don't also return word stems that we found.
    # the problem with this line, is it made it not work for a word like "helsingin"
    # sometimes that word stem is the right answer, lol . I made some changes around line 67, so that
    # a string equal to a word stem will stay in IF that's what the for loop at line 68 pooped out.
    #end_list = [a for a in end_list if a not in mediating_list_3]

    end_list = remove_copies(end_list)
    print("der end list")
    print(end_list)
    # Now checking if any of the potential answers happened to be participles
    mediated_list_4 = []
    kick_me_out = []
    for candidate in substitute_end_list:
        print(" candidate : %s" % candidate)
        kick_out_original = False
        mediating_list = post_processing(candidate)
        # this line was put in to fix the lemmatizer not getting words like onnistuneen
        if len(mediating_list) == 0:
            print("addings %s"%candidate)
            mediating_list.append(candidate)
        mediating_list_3 = []

        for mediated_candidate in mediating_list:
            print("mediated candidate : %s"%mediated_candidate)
            mediating_list_2 = verb_stem_to_lemma(mediated_candidate)
            mediating_list_3 += mediating_list_2
        mediating_list += mediating_list_3
        mediating_list_2 = return_past_participles(candidate)
       # So, with a word like tullut that tests positive as a past participle,
        # we will not need the original form as an answer.
        if len(mediating_list_2) >0:
            kick_out_original = True
        mediating_list += mediating_list_2
        mediating_list = remove_copies(mediating_list)
        mediating_list_2 = return_past_passive_participles(candidate)
        if len(mediating_list_2) >0:
            kick_out_original = True
        mediating_list += mediating_list_2
        mediating_list = remove_copies(mediating_list)
        for mediated_candidate_2 in mediating_list:
            mediated_list_4.append(mediated_candidate_2)
        if kick_out_original:
            kick_me_out.append(candidate)

    for mediated_4 in mediated_list_4:
        end_list.append(mediated_4)

    end_list = [a for a in end_list if a not in kick_me_out]

    basic steps:
    see if you had any nominal stems
    see if you had anything that was a present participle or different infinitive (post processing)
    see if you had any past participles
    see if you had any past passive participles
    ... what about present passive participles?


5
I'm adding a plural-lookahead to the nominal lemmatizer. This could easily cause some issues though. The idea, is that
if you have an affix like the genetive n , or the nominal plural t, you know that the word can't return plural stems.
the only thing, is there are words like kaunein and like instrumental words, that have a plural stem with what looks
like a genetive singular suffix. Maybe just undo the boolean?


6

I made superlatives catch mma as well, so that when hulluimmassa gives back the two possibilities, both get sucked in

This should be fine but it maybe it could have downstream  effects.

7
I don't know, do they do the V+N possessive marker after ksi? I voted no.
Yeah, so i made the hard_loc detector a regex dictionary


8

are there any verbs that end in aata? I think if a verb stem ends in aa, then the vta verb for it would be
ata , rather than aata... but if there are some that are aata, then maybe you don't want to goof with those.
look at line 501 or so in return forms, change the 2 back to a 1...

"""

