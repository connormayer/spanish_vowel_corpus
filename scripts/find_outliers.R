library(tidyverse)
data_file <- "C:/Users/conno/git_repos/spanish_vowel_corpus/data/results.csv"

# Base R has read.csv
df <- read_csv(data_file)

df %>%
  filter(!(Vowel %in% c('a', 'i', 'u', 'e', 'o')))
# 
# df_f <- filter(df, Gender == 'f')
# df_f <- select(df_f, 'F1_50', 'F2_50', 'Subject')
# df_f <- arrange(df_f, Subject)
# 
# df_f <- df %>%
#   filter(Gender == 'f') %>%
#   select('F1-50', 'F2-50', 'Subject') %>%
#   arrange(Subject)
# 
# ggplot(data = df) +
#   geom_point(aes(x = `F1-50`, y = `F2-50`, color=Vowel),
#              size = 10)
