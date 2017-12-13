from scipy import spatial
import pdb
from nltk.corpus import wordnet
import math
import numpy as np

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

            if s1_try == []:
                s1.append(0)
                s1_word.append('No match')
            else:
                #If the similarity is above the threshold then only include it
                s1_try = [x for x in s1_try if x is not None]
                if max(s1_try) > 0.2 :
                    ind = s1_try.index(max(s1_try))
                    s1.append(s1_try[ind])
                    s1_word.append(s1_word_try[ind])

                else :
                    s1.append(0)
                    s1_word.append('No match')

    word_order_vector = []
    for i in range(len(s1)) :
        #print("Original Word :", original_word[i] , "Matched Word :", s1_word[i], "Score : " , s1[i])
        #print("Iw1: " ,get_information(original_word[i], T))
        #print("Iw1bar: ", get_information(s1_word[i], T1.split()))
        #print(s1[i] * get_information(original_word[i], T) * get_information(s1_word[i], T1.split()))
        if s1_word[i] == "No match" :
            word_order_vector.append(0)
        else :
            word_order_vector.append(T1.index(s1_word[i]) + 1)

    return s1, word_order_vector

def get_information(sentence_list) :
    semantic_vector = []
    for word in sentence_list :
        word_count = sentence_list.count(word)
        semantic_vector.append(1 - (math.log(word_count + 1)/math.log(len(sentence_list) + 1)))
    return semantic_vector

def semantic_similarity(T1, T2) :
    #dataSetI = [0.390, 0.330, 0.179, 0.146, 0.239, 0.074, 0, 0.082, 0.1, 0, 0, 0, 0.263, 0.288]
    #dataSetII = [0.390, 0, 0.1, 0, 0, 0, 0.023, 0.479, 0.285, 0.075, 0.043, 0.354, 0.267, 0.321]
    return(1 - spatial.distance.cosine(T1, T2))

def word_order_similarity(r1, r2) :
    #r1 and r2 should be numpy array
    #r1 = np.array([1, 2, 3, 4, 5, 6, 0, 3, 3, 0, 0, 0, 1, 1])
    #r2 = np.array([4, 0, 3, 0, 0, 0, 1, 2, 3, 5, 6, 7, 8, 9])
    return 1.0 - (np.linalg.norm(r1 - r2) / np.linalg.norm(r1 + r2))

def overall_sentence_similarity(delta, Ss, Sr) :
    #Ss = 0.6139
    #Sr = 0.2023
    return((delta * Ss) + ((1-delta) * Sr))

if __name__ == '__main__' :
    T1 = "RAM keeps things being worked with"
    T2 = "The CPU uses RAM as a short term memory store"

    T = []
    # Combine words from both the sentences
    combined_list = T1.split() + T2.split()
    # Keep only unique words
    for word in combined_list:
        if word not in T:
            T.append(word)

    score1, word_order_vector1 = similarity_function(T1.split(), T)
    score2, word_order_vector2 = similarity_function(T2.split(), T)
    pdb.set_trace()
    semantic_vector1 = get_information(T1.split())
    semantic_vector2 = get_information(T2.split())
    #print(semantic_vector)
    Ss = semantic_similarity(semantic_vector1, semantic_vector2)
    Sr = word_order_similarity(word_order_vector1, word_order_vector2)

    delta = 0.85
    similarity_score = overall_sentence_similarity(delta, Ss, Sr)