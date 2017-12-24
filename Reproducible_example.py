import nltk
import pdb
from nltk.corpus import wordnet
import math
import numpy as np
import sys
from nltk.corpus import brown
from POSTagging import get_subject_object


#Defining constants
delta = 0.85
threshold = 0.2
ALPHA = 0.2
BETA = 0.45
ETA = 0.4
brown_freqs = dict()
N = 0



def semantic_similarity(sentence_1, sentence_2):

    info_content_norm = True
    words_1 = nltk.word_tokenize(sentence_1)
    words_2 = nltk.word_tokenize(sentence_2)
    joint_words = set(words_1).union(set(words_2))
    vec_1 = semantic_vector(words_1, joint_words, info_content_norm)
    vec_2 = semantic_vector(words_2, joint_words, info_content_norm)
    return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))


def semantic_vector(words, joint_words, info_content_norm):
    sent_set = set(words)
    semvec = np.zeros(len(joint_words))
    i = 0
    for joint_word in joint_words:
        if joint_word in sent_set:
            # if word in union exists in the sentence, s(i) = 1 (unnormalized)
            semvec[i] = 1.0
            if info_content_norm:
                semvec[i] = semvec[i] * math.pow(info_content(joint_word), 2)
        else:
            # find the most similar word in the joint set and set the sim value
            sim_word, max_sim = most_similar_word(joint_word, sent_set)
            semvec[i] = threshold if max_sim > threshold else 0.0
            if info_content_norm:
                semvec[i] = semvec[i] * info_content(joint_word) * info_content(sim_word)
        i = i + 1
    return semvec

def most_similar_word(word, word_set):
    max_sim = -1.0
    sim_word = ""
    for ref_word in word_set:
      sim = word_similarity(word, ref_word)
      if sim > max_sim:
          max_sim = sim
          sim_word = ref_word
    return sim_word, max_sim

def word_similarity(word_1, word_2):
    synset_pair = get_best_synset_pair(word_1, word_2)
    return (length_dist(synset_pair[0], synset_pair[1]) *
        hierarchy_dist(synset_pair[0], synset_pair[1]))

def get_best_synset_pair(word_1, word_2):
    synsets_1 = wordnet.synsets(word_1)
    synsets_2 = wordnet.synsets(word_2)
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
                sim = wordnet.path_similarity(synset_1, synset_2)
                if sim != None and sim > max_sim:
                    max_sim = sim
                    best_pair = synset_1, synset_2
        return best_pair

def length_dist(synset_1, synset_2):
    l_dist = sys.maxsize
    if synset_1 is None or synset_2 is None:
        return 0.0
    if synset_1 == synset_2:
        # if synset_1 and synset_2 are the same synset return 0
        l_dist = 0.0
    else:
        wset_1 = set([str(x.name()) for x in synset_1.lemmas()])
        wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
        if len(wset_1.intersection(wset_2)) > 0:
            # if synset_1 != synset_2 but there is word overlap, return 1.0
            l_dist = 1.0
        else:
            # just compute the shortest path between the two
            l_dist = synset_1.shortest_path_distance(synset_2)
            if l_dist is None:
                l_dist = 0.0
    # normalize path length to the range [0,1]
    return math.exp(-ALPHA * l_dist)

def hierarchy_dist(synset_1, synset_2):
    h_dist = sys.maxsize
    if synset_1 is None or synset_2 is None:
        return h_dist
    if synset_1 == synset_2:
        # return the depth of one of synset_1 or synset_2
        h_dist = max([x[1] for x in synset_1.hypernym_distances()])
    else:
        # find the max depth of least common subsumer
        hypernyms_1 = {x[0]: x[1] for x in synset_1.hypernym_distances()}
        hypernyms_2 = {x[0]: x[1] for x in synset_2.hypernym_distances()}
        lcs_candidates = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(lcs_candidates) > 0:
            lcs_dists = []
            for lcs_candidate in lcs_candidates:
                lcs_d1 = 0
                if lcs_candidate in hypernyms_1:
                    lcs_d1 = hypernyms_1[lcs_candidate]
                lcs_d2 = 0
                if lcs_candidate in hypernyms_2:
                    lcs_d2 = hypernyms_2[lcs_candidate]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) /
            (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))


def info_content(lookup_word):
    global N
    if N == 0:
        for sent in brown.sents():
            for word in sent:
                word = word.lower()
                if word not in brown_freqs:
                    brown_freqs[word] = 0
                brown_freqs[word] = brown_freqs[word] + 1
                N = N + 1
    lookup_word = lookup_word.lower()
    n = 0 if lookup_word not in brown_freqs else brown_freqs[lookup_word]
    return 1.0 - (math.log(n + 1) / math.log(N + 1))


def similarity_function(T1, T) :

    s1 = []
    s1_word = []
    original_word = []
    #For every word in T, find it's closest counterpart in the sentence
    for s2 in T :
        original_word.append(s2)
        if s2 in T1 :
            s1.append(1)
            s1_word.append(s2)
        else :
            s1_try = []
            s1_word_try = []
            w1 = wordnet.synsets(s2)
            for sys in w1 :
                for t1_word in T1 :
                    w2 = wordnet.synsets(t1_word)
                    for t1_syn in w2 :
                        s1_try.append(sys.wup_similarity(t1_syn))
                        s1_word_try.append(t1_word)

            s1_try = [x for x in s1_try if x is not None]
            if s1_try == []:
                s1.append(0)
                s1_word.append('No match')
            else:
                #If the similarity is above the threshold then only include it
                if max(s1_try) > threshold :
                    ind = s1_try.index(max(s1_try))
                    s1.append(s1_try[ind])
                    s1_word.append(s1_word_try[ind])

                else :
                    s1.append(0)
                    s1_word.append('No match')

    word_order_vector = []
    for i in range(len(s1)) :
        if s1_word[i] == "No match" :
            word_order_vector.append(0)
        else :
            word_order_vector.append(T1.index(s1_word[i]) + 1)

    return word_order_vector

def get_information(sentence_list) :
    semantic_vector = []
    for word in sentence_list :
        word_count = sentence_list.count(word)
        semantic_vector.append(1 - (math.log(word_count + 1)/math.log(len(sentence_list) + 1)))
    return semantic_vector

def word_order_similarity(r1, r2) :
    #r1 and r2 should be numpy array
    return 1.0 - (np.linalg.norm(r1 - r2) / np.linalg.norm(r1 + r2))

def overall_sentence_similarity(Ss, Sr) :
    return((delta * Ss) + ((1-delta) * Sr))

def get_POS_score(T1, T2) :
    subject1, object1 = get_subject_object(T1)
    subject2, object2 = get_subject_object(T2)
    subject1.extend(object1)
    subject2.extend(object2)
    common_elemnts = list(set(subject1).intersection(subject2))
    pos_score = 1 if len(common_elemnts) > 0 else 0
    return pos_score


def combine_main(T1, T2) :
    T = []
    # Combine words from both the sentences
    combined_list = T1.split() + T2.split()
    # Keep only unique words
    for word in combined_list:
        if word not in T:
            T.append(word)

    word_order_vector1 = similarity_function(T1.split(), T)
    word_order_vector2 = similarity_function(T2.split(), T)
    Sr = word_order_similarity(np.array(word_order_vector1), np.array(word_order_vector2))

    Ss = semantic_similarity(T1, T2)
    similarity_score = overall_sentence_similarity(Ss, Sr)
    if similarity_score < 0.5 :
        similarity_score = get_POS_score(T1, T2)

    return similarity_score

if __name__ == '__main__' :
    T1 = "RAM keeps things being worked with"
    T2 = "The CPU uses RAM as a shortterm memory store"
    similarity_score = combine_main(T1, T2)