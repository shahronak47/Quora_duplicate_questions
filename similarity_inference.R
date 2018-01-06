df$answer <- ifelse(df$similarity_score > 0.5, 1, 0)
table(df$answer == df$is_duplicate)/nrow(df)

#FALSE      TRUE 
#0.3465347 0.6534653 

#Get wrong solutions
new_df <- df[df$answer != df$is_duplicate, ]
write.csv(new_df, "/Users/ronakshah/Downloads/wrong_answer_2_sample.csv")



