import re
import spacy
import pdb

def get_subject_object (sentence) : 
    #Load the english language
    nlp = spacy.load('en')
    doc = nlp(sentence)
    subject = []
    object = []
    for tok in doc :
        print(tok.lemma_, tok.text, tok.dep_, tok.tag_)
        #Search for token having subj in them
        #if re.search('subj', tok.dep_) :
            #Get the corresponding words
        #    subject.append(tok.lemma_)
        # Search for token having obj in them
        #if re.search('obj', tok.dep_) :
        #    object.append(tok.lemma_)

    return subject, object

if __name__ == '__main__' : 
    T1 = "Where can I find a European family office database?"
    T2 = "Can I make 50,000 a month by day trading?"
    get_subject_object(T2)