from lists_and_dictionaries import *




def ends_in(checkable,ending):
    if len(checkable) > len(ending):
        if checkable[len(checkable)-len(ending):] == ending:
            return True,checkable[0:len(checkable)-len(ending)]
        else:
            return False,checkable[0:len(checkable)-len(ending)]
    else:
        return False,checkable

def count_syllables(word):
    syllable_count = 0
    index = 0
    while index < len(word):
        if word[index] in vowels:
            if index+1 <= len(word)-1:
                if word[index] not in ['a','ä'] and word[index+1] in ['a','ä']:

                    syllable_count += 2
                    if index+2 <= len(word)-1:
                        if word[index+2] == "i":
                            index += 3
                        else:
                            index += 2
                    else:
                        index +=2
                elif word[index +1] in vowels:
                    syllable_count += 1
                    index +=2
                else:
                    syllable_count += 1
                    index +=1
            else:
                syllable_count +=1
                index +=1
        else:
            index +=1
    return syllable_count



def take_first_syllable(word):
    stop = False
    vowel_yet = False
    answer = ""
    index = 0
    while stop == False:
        letter = word[index]
        #print("Our letter is %s"%(letter))
        next_letter = None
        if len(word)-1 >= index +1:
            next_letter = word[index+1]

        if letter in vowels:
            vowel_yet = True
            if next_letter == None:
                answer += letter
                stop = True
                #print("taking pathway 1")
                break
            elif next_letter in vowels:
                # this is for non diphthongal vowel combos
                if (letter not in ['a','ä'] and next_letter in ['a','ä']) or \
                        (letter not in ['o','ö'] and next_letter in ['o','ö']):

                    answer += letter
                    index += 1
                    #print("taking pathway 2")
                    stop = True
                    break
                # If it's part one of a regular old diphthong
                else:
                    #print("taking pathway 3")
                    answer += letter
            else:
                #print("taking pathway 4")
                answer += letter
        # Now, dealing with postvocalic consonants.
        elif vowel_yet:
            if next_letter == None:
                #print("taking pathway 5")
                answer += letter
                stop = True
                break
            elif next_letter in vowels:
                #print("taking pathway 6")
                stop = True
                break
            else:
                #print("taking pathway 7")
                answer += letter
                index += 1
                stop = True
                break

        # prevocalic consonants
        else:
            #print("taking pathway 8")
            answer += letter
        if next_letter == None:
            #print("taking pathway 9")
            stop = True
            break
        else:
            index +=1
    chopped_word = ""
    if index < len(word)-1:
        #print("the prophecy is true")
        #print(index)
        #print(len(word))
        chopped_word = word[index:]
    #print(index)
    return answer,chopped_word
def return_syllables(word):
    end_list = []
    word_so_far = word
    while word_so_far != "":
        first,remainder = take_first_syllable(word_so_far)
        end_list.append(first)
        word_so_far = remainder
    return end_list

def consonant_gradation_harden(word):
    # checks to see if the final syllable could have been
    # subject to consonant gradation and returns the alternative,
    # alongside its original.
    # e.g. Lammu becomes Lampu
    # Also, it tells you if consonant gradation was necessary on the word.
    necessary_to_apply = False
    did_anything_happen = False
    original_word = word
    end_word = ""
    representation = return_syllables(word)
    if len(representation)>1:
        # first check for doubles
        first_of_last = representation[len(representation)-1][0]
        last_of_second_to_last = representation[len(representation)-2][len(representation[len(representation)-2])-1]
        fusion = last_of_second_to_last + first_of_last
        if fusion in softened_hash:
            if fusion in necessary_to_harden:
                necessary_to_apply = True
            #now, return the hardened version.
            new_first_of_last = softened_hash[fusion][1]
            new_last_of_second_to_last = softened_hash[fusion][0]
            if len(representation[len(representation) - 1]) > 1:
                representation[len(representation) - 1]= new_first_of_last + representation[len(representation)-1][1:]
            # this line shouldn't be necessary.. the first letter of the combination is the same
            #representation[len(representation) - 2][len(representation[len(representation) - 2]) - 1] = new_last_of_second_to_last
            for syllable in representation:
                end_word += syllable
        elif first_of_last in softened_hash and (last_of_second_to_last in vowels or last_of_second_to_last =='h'):
            if first_of_last in necessary_to_harden:
                necessary_to_apply = True
            new_first_of_last = softened_hash[first_of_last]
            if len(representation[len(representation)-1]) > 1:
                representation[len(representation) - 1]= new_first_of_last + representation[len(representation)-1][1:]
            else:
                pass
            for syllable in representation:
                end_word += syllable
        else:
            pass
    else:
        pass
    if end_word != "":
        did_anything_happen = True

    return did_anything_happen,necessary_to_apply,original_word,end_word,

def consonant_gradation_soften(word):
    # checks to see if the final syllable could have been
    # subject to consonant gradation and returns the alternative,
    # alongside its original.
    # e.g. Lammu becomes Lampu
    original_word = word
    end_word = ""
    representation = return_syllables(word)
    if len(representation)>1:
        # first check for doubles
        # this whole, first two of last thing is really for the word startata. Maybe there are more like it?
        first_two_of_last = representation[len(representation) - 1][:2]
        first_of_last = representation[len(representation)-1][0]
        last_of_second_to_last = representation[len(representation)-2][len(representation[len(representation)-2])-1]
        fusion = last_of_second_to_last + first_of_last

        if first_two_of_last in hardened_hash:
            print(representation[len(representation)-1][1:])
            new_first_two_of_last = first_of_last[0]
            if len(representation[len(representation) - 1]) > 1:
                representation[len(representation) - 1]= new_first_two_of_last + representation[len(representation)-1][2:]
            # this line shouldn't be necessary.. the first letter of the combination is the same
            #representation[len(representation) - 2][len(representation[len(representation) - 2]) - 1] = new_last_of_second_to_last
            for syllable in representation:
                end_word += syllable

        elif fusion in hardened_hash:
            #now, return the hardened version.
            if len(hardened_hash[fusion])>1:
                new_first_of_last = hardened_hash[fusion][1]
            else:
                new_first_of_last = ""
            new_last_of_second_to_last = hardened_hash[fusion][0]
            if len(representation[len(representation) - 1]) > 1:
                representation[len(representation) - 1]= new_first_of_last + representation[len(representation)-1][1:]
            # this line shouldn't be necessary.. the first letter of the combination is the same
            #representation[len(representation) - 2][len(representation[len(representation) - 2]) - 1] = new_last_of_second_to_last
            for syllable in representation:
                end_word += syllable
        elif first_of_last in hardened_hash and last_of_second_to_last != "s":
            new_first_of_last = hardened_hash[first_of_last]
            if len(representation[len(representation)-1]) > 1:
                representation[len(representation) - 1]= new_first_of_last + representation[len(representation)-1][1:]
            else:
                pass
            for syllable in representation:
                end_word += syllable
        else:
            pass
    else:
        pass

    return original_word,end_word


def detect_harmony(word):
    # This doesn't work for compound words that have the first part belonging to one harmony group, and
    # that have the second part belonging to the other. But for my purposes, I do not believe I need that because
    # this would only give an issue for verbs, the vast majority of which are not compound in nature, and thus
    # do not allow for that kind of a mix-up.

    # If I have added an a to a word that I should have added an ä to the end of,
    # this function will help rectify that.
    # what this function does, is tell you whether the word is a front vowel word, a back vowel word, or a neutral
    # word, by returning true, false, or None respectively.
    back_vowels = ['a','o','u']
    front_vowels = ['ä','ö','y']
    answer = None
    index = 0
    while index < len(word):
        if word[index] in back_vowels:
            return False
        elif word[index] in front_vowels:
            return True
        else:
            pass
        index +=1
    return (answer)


def remove_copies(sample_list):
    new_list = []
    for element in sample_list:
        if element not in new_list:
            new_list.append(element)
    return (new_list)

def correct_for_harmony(sample_list,ending):
    correspondences = {"a":"ä", "ä":"a","o":"ö","ö":"o","u":"y","y":"u"}
    end_list = []
    reverse_ending =""
    for letter in ending:
        if letter in correspondences:
            reverse_ending+= correspondences[letter]
        else:
            reverse_ending+= letter

    for member in sample_list:
        boolean,word = ends_in(member,ending)
        if detect_harmony(word)== detect_harmony(ending) or boolean == False:
            end_list.append(member)
        elif detect_harmony(word)!= detect_harmony(ending):
            if detect_harmony(word)== None:
                end_list.append(member)
                end_list.append(word+reverse_ending)
            else:
                end_list.append(word+reverse_ending)
    return(end_list)