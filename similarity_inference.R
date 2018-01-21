df$answer <- ifelse(df$similarity_score > 0.5, 1, 0)
table(df$answer == df$is_duplicate)/nrow(df)
#FALSE      TRUE 
#0.3465347 0.6534653 

#FALSE      TRUE 
#0.3465347 0.6534653 

#FALSE      TRUE 
#0.3465347 0.6534653 

#Get wrong solutions
new_df <- df[df$answer != df$is_duplicate, ]
write.csv(new_df, "C:\\Users\\Ronak Shah\\Google Drive\\Quora_duplicate_questions\\wrong_answers.csv")


sort(table(cut(wrong_answers$similarity_score, breaks = seq(0, 1, 0.1))))

#(0,0.1] (0.1,0.2] (0.2,0.3]   (0.9,1] (0.3,0.4] (0.4,0.5] (0.8,0.9] (0.7,0.8] (0.6,0.7] (0.5,0.6] 
#146       804      3344      5443      7474     15044     21077     24987     29022     34966 

#Get right solutions
new_df <- df[df$answer == df$is_duplicate, ]
write.csv(new_df, "C:\\Users\\Ronak Shah\\Google Drive\\Quora_duplicate_questions\\wrong_answers.csv")
sort(table(cut(new_df$similarity_score, breaks = seq(0, 1, 0.1))))

#(0,0.1]   (0.9,1] (0.5,0.6] (0.1,0.2] (0.8,0.9] (0.6,0.7] (0.7,0.8] (0.2,0.3] (0.3,0.4] (0.4,0.5] 
#4923     15510     23449     23723     25844     28421     29226     35604     37580     37665 


#Get one/two word difference questions
write.csv(new_df, "/Users/ronakshah/Downloads/wrong_answer_2_sample.csv")

#library(stringr)
#close_df <- df[abs(str_count(df$question1, " ") - str_count(df$question2, " ")) < 3, ]
head_df = head(df)
library(stringi)

get_different_words <- function(a, b) {
  length(Reduce(setdiff,stri_extract_all_regex(c(a, b),"\\w+"))) < 3
}
close_df = df[apply(df, 1, function(x) get_different_words(x['question1'], x['question2'])), ]
write.csv(close_df, "C:\\Users\\Ronak Shah\\Google Drive\\Quora_duplicate_questions\\close_questions.csv")
