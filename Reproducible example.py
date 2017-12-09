import pandas as pd
from nltk.corpus import wordnet

T1 = "RAM keeps things being worked with"
T2 = "The CPU uses RAM as a short term memory store"

T = []
combined_list = T1.split() + T2.split()

for word in combined_list :
    if word not in T :
        T.append(word)