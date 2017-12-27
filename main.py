from Reproducible_example import combine_main
import pandas as pd
import pdb

if __name__ == '__main__' :
    df = pd.read_csv("quora_duplicate_questions.csv")
    df = df.ix[0:100, ]
    similarity_score = []
    for index, row in df.iterrows() :
#        try :
        print(index)
        similarity_score.append(combine_main(row['question1'], row['question2']))
#        except :
#            similarity_score.append(0)
            
    df['similarity_score'] = similarity_score
    df.to_csv('Answers.csv')


