import pdb
from nltk.corpus import wordnet


def similarity_function() :
    T1 = "RAM keeps things being worked with"
    T2 = "The CPU uses RAM as a short term memory store"

    T = []
    combined_list = T1.split() + T2.split()

    for word in combined_list :
        if word not in T :
            T.append(word)

    s1 = []
    s1_word = []
    original_word = []
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
                for t1_word in T1.split() :
                    w2 = wordnet.synsets(t1_word)
                    for t1_syn in w2 :
                        s1_try.append(sys.wup_similarity(t1_syn))
                        s1_word_try.append(t1_word)

            if s1_try == []:
                s1.append(0)
                s1_word.append('No match')
            else:
                ind = s1_try.index(max(s1_try))
                s1.append(s1_try[ind])
                s1_word.append(s1_word_try[ind])


    for i in range(len(s1)) :
        print("Original Word :", original_word[i] , "Matched Word :", s1_word[i], "Score : " , s1[i])

if __name__ == '__main__' :
    similarity_function()

