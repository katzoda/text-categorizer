#!/usr/bin/env python3

# 1. read the parts of speech files into the individual lists
# verbs, adverbs, adjectives, pronouns, prepositions, conjunctions

import glob, random

# It's reading files with lists of parts of speech in local directory. File names ending with *list.txt
file_list = glob.glob("parts_of_speech/*list.txt")

def word_uploader(file):

    word_list = []
    with open(file, mode="r") as f:
        for word in f.readlines():
            word_list.append(word.strip())
    return word_list


for file in file_list:
    result_list = word_uploader(file)
    if file == "parts_of_speech/verbs_list.txt":
        verbs = result_list
    elif file == "parts_of_speech/adverbs_list.txt":
        adverbs = result_list
    elif "adjective" in file:
        adjectives = result_list
    elif "pronoun" in file:
        pronouns = result_list
    elif "prepo" in file:
        prepositions = result_list
    elif "conjunct" in file:
        conjunctions = result_list
    elif "spec_char" in file:
        spec_chars = result_list
    else:
        print("File not found")

num_chars = ['0','1','2','3','4','5','6','7','8','9']
alphabet = "abcdefghijklmnopqrstuvwxyz"


###############################

# Read the input file and process special characters

###############################

#input_file = "paris_article.txt"
input_file = "usa_elec.txt"
text_list = []
text_words = []

with open(input_file, mode='r') as text:
    for line in text.readlines():
        line = line.split()
        if len(line) > 0:
            for word in line:
                text_words.append(word)


words= []
numbers = []

def word_constructor(i, word):
    if i == 0:
        rec = word[1:]
    elif i == len(word) - 1:
        rec = word[:-1]
    else:
        rec = word[:i] + word[i+1:]
    return rec


for word in text_words:
    # Count how many spec char and num_chars in individual words
    c = 0
    n = 0
    a = 0
    for letter in word:
        if letter in spec_chars:
            c += 1
        if letter in num_chars:
            n += 1
        if letter in alphabet:
            a += 1

    # I'll need to use this counter more times due to decrementing it during while loops
    c1 = c
    c2 = c

    # the word is a string
    if c == 0 and n == 0:
        words.append(word)

    # only spec chars and no number in the string
    elif c > 0 and n == 0:

        # While there is a special character in word keep looping
        # When c is decreased to 0 the word is stripped off of all special characters
        while c > 0:
            for i, letter in enumerate(word):
                if letter in spec_chars:
                    # The special char is either at beginning or in the middle or at the end of the word
                    word_rec = word_constructor(i, word)

            c -= 1

        # Reconstructed string word_rec is assigned to variable word so new version of word can enter the loop over and over again
            word = word_rec

        words.append(word_rec)

    # Only numbers with or without spec characters
    elif a == 0 and n > 0:

        # the word is an integer number (not a float)
        if c1 == 0:
            numbers.append(int(word))

        elif c1 > 0 and "." in word[:-1]:
            # to store index position of a dot in float number
            dot_index = 0
            first_char = ""
            w_len = len(word)

            while c1 > 0:
                
                for i, num in enumerate(word):
                    # if first_char is not a number the dot_index will need to be decreased by 1 when putting the dot back
                    first_char = word[0]

                    if num in spec_chars:
                        # I need to store index position of the dot when at the same time the dot is not the last character
                        if num == "." and i != w_len - 1:
                            dot_index = i 
                for i, num in enumerate(word):
                    if num in spec_chars:
                        num_rec = word_constructor(i, word)

                word = num_rec
                c1 -= 1

            # putting the dot back  56.789 or (56.789)
            if first_char in spec_chars:
                dot_index = dot_index - 1
                num_rec = num_rec[:dot_index] + "." + num_rec[dot_index:]
            elif first_char in num_chars:
                num_rec = num_rec[:dot_index] + "." + num_rec[dot_index:]

            numbers.append(float(num_rec))


        elif c2 > 0 and "." not in word[:-1]:
            while c2 > 0:
                for i, num in enumerate(word):
                    if num in spec_chars:
                        num_rec = word_constructor(i, word)

                c2 -= 1

            # Reconstructed string word_rec is assigned to variable word so new version of word can enter the loop over and over again
                word = num_rec

            numbers.append(int(num_rec))



###############################

# ANALYSIS

###############################

# Check the input text against all the parts of the speech lists
# verbs, adverbs, adjectives, pronouns, prepositions, conjunctions

verbs_out=[]
adverbs_out=[]
adjectives_out=[]
pronouns_out=[]
prepositions_out=[]
conjunctions_out=[]
nouns_out=[]
names = []
catch_me = []

def word_sorter(word):
    word = word.lower()
    if word in verbs:
        verbs_out.append(word)
    elif word in adverbs:
        adverbs_out.append(word)
    elif word in adjectives:
        adjectives_out.append(word)
    elif word in pronouns:
        pronouns_out.append(word)
    elif word in prepositions:
        prepositions_out.append(word)
    elif word in conjunctions:
        conjunctions_out.append(word)
    else:
        nouns_out.append(word)

for word in words:
    try:
        # Trying to extract names of people and places
        if word[0] == word[0].upper():
            names.append(word)
        else:
            word_sorter(word)
    except AttributeError:
        catch_me.append(word)
    except IndexError:
        catch_me.append(word)



# Filtering words with capital letter other than nouns. Than lower casing all words anyway and adding them to nouns list -
# because they are actually nouns
for name in names:
    word_sorter(name)

all_lists = [
    verbs_out,
    adverbs_out,
    adjectives_out,
    pronouns_out,
    prepositions_out,
    conjunctions_out,
    nouns_out
]

# Removing some leftovers like prepositions, conjunctions etc. (except nouns)
# So name list contains names and still other nouns with capital letter (so it's not entirely perfect)
for ls in all_lists[:-1]:
    for name in names:
        new_name = name.lower()
        if new_name in ls:
            names.remove(name)

list_strings = ['VERBS', 'ADVERBS', 'ADJECTIVES', 'PRONOUNS', 'PREPOSITIONS', 'CONJUCTIONS', 'NOUNS']
list_counter = 0

# The total number of words or elements (split based on whitespace); attained before any processing or separation
total_num_words = len(text_words)


for ls in all_lists:

    # Percentage / len(ls) + len(names)
    percentage = (len(ls) / (total_num_words - len(numbers))) * 100
    percentage = round(percentage, 2)

    # Max occurrence
    if len(ls) > 0:
        unique_words = set(ls)
        max_occurrence = {}

        # constructing the dictionary where key is the word and value its frequency in the text (in a particular part of speech list)
        for w in unique_words:
            max_occurrence[w] = ls.count(w)

        word_keys = []
        word_values = []
        max_values_index = []
        max_occurrence_words = []

        # Unpacking the dictionary
        for key, val in max_occurrence.items():
            word_keys.append(key)
            word_values.append(val)

        max_val = max(word_values)

        # what index position has the max value in word_values list
        for i, w_val in enumerate(word_values):
            if w_val == max_val:
                max_values_index.append(i)

        # Match the index of the highest frequency with the actual word (stored in word_keys - unpacked from max_occurence dict)
        for i in max_values_index:
            max_occurrence_words.append(word_keys[i])
    else:
        max_occurrence_words = []
        max_val = 0

    print("*"*100)
    print(f"Number of {list_strings[list_counter]}: {len(ls)} ---->  {percentage} % of all words.\n")
    if max_val:
        print(f"The most used word(s) are: {'  '.join(max_occurrence_words)}")
        print("")
        print(f"Frequency: {max_val} time(s).")
    else:
        print("")
    print("")
    print("*"*100)
    list_counter += 1

print("*"*100)
print(f"Numbers in the text: {numbers}")

########################

#  Analyzer tells the user what the text is all about :)

########################

print("")
print("")
print("Now follows the summary. Please be aware. If your text is sensitive the outcome may seem funny and therefore inappropriate.")
print("")
user_input = input("Do you want to proceed? Please type Y or N:")

if user_input.lower() == "y":

    def random_word(part_speech):
        return part_speech[random.randint(0, len(part_speech) - 1)]


    print("")
    print("What is the text about?")
    print("")
    print(f"This text contains {total_num_words} elements. The main topic covers mostly {random_word(nouns_out)}.")
    print(f"If there are any persons the text mentions mainly {random_word(names)}, {random_word(names)} and some {random_word(names)}.")
    print("")
    print("")
    print("Warning. Following text may be nonsense. But it may give the reader a deeper insight into the main topic of the text.")
    print("")
    print(f"{random_word(nouns_out).title()} {random_word(verbs_out)} {random_word(prepositions_out)} {random_word(names)}.", end="")
    print(f" {random_word(pronouns_out).title()} {random_word(verbs_out)} {random_word(conjunctions_out)} the {random_word(names)} {random_word(verbs_out)} to go to {random_word(nouns_out)}.")
    print(f"{random_word(nouns_out).title()} {random_word(conjunctions_out)} {random_word(nouns_out)} {random_word(verbs_out)} {random_word(prepositions_out)} {random_word(names)}.")
    print("")
else:
    print("")
    print("Thank You and Goob Bye.")
    print("")
