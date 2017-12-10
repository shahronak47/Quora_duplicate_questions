import pdb
from nltk.corpus import wordnet
import math

def similarity_function(T1, T2, T) :

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

    print(word_order_vector)

def get_information(word, sentence_list) :

    word_count = sentence_list.count(word)
    return(1 - (math.log10(word_count + 1)/math.log10(len(sentence_list) + 1)))

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

    similarity_function(T1.split(), T2.split(), T)
    #semantic_vector = get_information(T)
    #print(semantic_vector)