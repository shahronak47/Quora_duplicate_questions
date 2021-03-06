import re
import spacy
import pandas as pd
import pdb

def get_subject_object (sentence) : 
    #Load the english language
    nlp = spacy.load('en')
    doc = nlp(sentence)
    subject = []
    object = []
    for tok in doc :
        #print(tok.lemma_, tok.text, tok.dep_, tok.tag_)
        #Search for token having subj in them
        if re.search('subj', tok.dep_) :
            #Get the corresponding words
            subject.append(tok.lemma_)
        # Search for token having obj in them
        if re.search('obj', tok.dep_) :
            object.append(tok.lemma_)

    return subject, object

if __name__ == '__main__' :
    df = pd.read_csv('close_questions.csv')
    df['subject1'] = ""
    df['subject2'] = ""
    df['object1'] = ""
    df['object2'] = ""
    
    for index, row in df.iterrows():
        try : 
            print(index)
            df.at[index, 'subject1'], df.at[index, 'object1'] = get_subject_object(row['question1'])
            df.at[index, 'subject2'], df.at[index, 'object2'] = get_subject_object(row['question2'])
            print(df.ix[index]['subject1'], df.ix[index]['subject2'], df.ix[index]['object1'], df.ix[index]['object2'])
        except :
            continue
        
    df.to_csv('Close_questions_with_subject_object.csv')