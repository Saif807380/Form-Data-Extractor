#!/usr/bin/env python
# coding: utf-8
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import sys
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')

stopwords = list(STOP_WORDS)

def calc_word_frequencies(doc):
    print(type(doc))
    word_frequencies = {}
    for word in doc:
        if word.text not in stopwords and word.text not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    return word_frequencies

def get_max_frequency(word_frequencies):
    return max(word_frequencies.values())

def normalize_word_frequencies(word_frequencies):
    max_frequency = get_max_frequency(word_frequencies)
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/max_frequency)
    return word_frequencies

def get_sent_scores(sentence_list,word_frequencies):
    sentence_scores = {}  
    for i,sent in enumerate(sentence_list):  
        for word in sent:
            if word.text in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = [word_frequencies[word.text],i]
                else:
                    sentence_scores[sent][0] += word_frequencies[word.text]
    return sentence_scores

def generate_summary(doc,sents_in_summary):
    #print('sents_in_summary: ', type(sents_in_summary))
    word_frequencies = calc_word_frequencies(doc)
    word_frequencies = normalize_word_frequencies(word_frequencies)
    sentence_scores = get_sent_scores([sent for sent in doc.sents],word_frequencies)
    
    #sorting according to decreasing order of importance and choosing the first (sents_in_summary) sentences
    summarized_sentences = sorted(sentence_scores.items(),key=lambda x: x[1],reverse=True)[:sents_in_summary]
    
    #sorting according to appearance of sentences in the original text
    summarized_sentences = sorted(summarized_sentences,key=lambda x: x[1][1])
    
    final_sentences = [x[0].text.capitalize() for x in summarized_sentences]
    summary = " ".join(final_sentences)
    return summary









# doc = '''In the distant past, many people thought bats had magical powers, but times
# have changed. Today, many people believe that bats are rodents, that they cannot
# see, and that they are more likely than other animals to carry rabies. All of these
# beliefs are mistaken. Bats are not rodents, are not blind, and are no more likely
# than dogs and cats to transmit rabies. Bats, in fact, are among the least understood
# and least appreciated of animals.
# Bats are not rodents with wings, contrary to popular belief. Like all rodents, bats
# are mammals, but they have a skeleton similar to the human skeleton. The bones in
# bat wings are much like those in arms and the human hand, with a thumb and four
# fingers. In bats, the bones of the arms and the four fingers of the hands are very
# long. This bone structure helps support the web of skin that stretches from the body
# to the ends of the fingers to form wings.t
# Although bats cannot see colors, they have good vision in both dim and bright
# light. Since most bats stay in darkness during the day and do their feeding at night,
# they do not use their vision to maneuver in the dark but use a process called
# echolocation. This process enables bats to emit sounds from their mouths that bounce
# off objects and allow them to avoid the objects when flying. They use this system to
# locate flying insects to feed on as well. Typically, insect-eating bats emerge at dusk
# and fly to streams or ponds where they feed. They catch the insects on their wingtip
# or tail membrane and fling them into their mouths while flying.
# There are about 1,000 species of bat, ranging in size from the bumblebee bat,
# which is about an inch long, to the flying fox, which is sixteen inches long and has a
# wingspan of five feet. Each type of bat has a specialized diet. For seventy percent
# of bats, the diet is insects. Other types of bats feed on flowers, pollen, nectar, and
# fruit or on small animals such as birds, mice, lizards, and frogs.
# One species of bat feeds on the blood of large mammals. This is the common
# vampire bat, which lives only in Latin America and is probably best known for
# feeding on the blood of cattle. Unfortunately, in an attempt to control vampire bat
# populations, farmers have unintentionally killed thousands of beneficial fruit-and
# insect-eating bats as well.
# Bats, in fact, perform a number of valuable functions. Their greatest economic
# value is in eliminating insect pests. Insect- eating bats can catch six hundred
# mosquitoes in an hour and eat half their body weight in insects every night. In many
# tropical rain forests, fruit-eating bats are the main means of spreading the seeds of
# tropical fruits. Nectar-feeding bats pollinate a number of tropical plants. If it were
# not for bats, we might not have peaches, bananas, mangoes, guavas, figs, or dates.
# Today, the survival of many bat species is uncertain. Sixty percent of bats do not
# survive past infancy. Some are killed by predators such as owls, hawks, snakes and
# other meat-eating creatures, but most are victims of pesticides and other human
# intrusions. In Carlsbad Caverns, New Mexico, where there were once eight million
# bats, there are now a quarter million. At Eagle Creek, Arizona, the bat population
# dropped from thirty million to thirty thousand in six years.
# Bats often have been burdened with a bad reputation, perhaps because they
# are not the warm, cuddly sort of animal we love to love. However, their unusual
# physical features should not lead us to overestimate their harm or to underestimate
# their value.'''

# doc = '''INCOME TAX DEPARTMENT
# GOVT. OF INDIA
# Permanent Account Number Card
# FFCPP4452K
# TH /Name
# MOHAMMED MEHDI PATEL
# funIT aT TH / Father's Name
# ALIRAZA PATEL
# Date of Birth
# 02/08/2000
# BAER /Signature'''

# doc = nlp(doc.lower())

# tokens = [token for token in doc]

# sents_in_summary = 2
# summary = generate_summary(doc,sents_in_summary)






