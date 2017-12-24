import re
import spacy

def get_subject_object (sentence) :
    #T1 = "RAM keeps things being worked with"
    #T2 = "The CPU uses RAM as a shortterm memory store"
    #Load the english language
    nlp = spacy.load('en')
    doc = nlp(sentence)
    subject = []
    object = []
    for tok in doc :
        #Search for token having subj in them
        if re.search('subj', tok.dep_) :
            #Get the corresponding words
            subject.append(tok.text)
        # Search for token having obj in them
        if re.search('obj', tok.dep_) :
            object.append(tok.text)

    return subject, object
