import re
import spacy

if __name__ == '__main__' :
    T1 = "RAM keeps things being worked with"
    T2 = "The CPU uses RAM as a shortterm memory store"
    #Load the english language
    nlp = spacy.load('en')
    doc = nlp(T2)
    subject_object = []
    for tok in doc :
        #Search for token having subjects or object in them
        if re.search('subj|obj', tok.dep_) :
            #Get the corresponding words
            subject_object.append(tok.text)
    print(subject_object)
