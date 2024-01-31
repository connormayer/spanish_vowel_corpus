#install.packages("tidyverse")
library(tidyverse, warn.conflicts = FALSE)


# PART I: Importing Data
# Import the CSV (exported from Praat) and subset it. Create Vowel & Word lists
# for data clean up.

setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
df <- read_csv("results.csv", 
               na=c("","NA", "--undefined--")) # Data has missing entries
                                             # na sets all entries as NA values
df_50 <- df %>%
  select(Filename, Subject, Vowel, Word, F0, ends_with("_50"), F4, Duration)
  # Pick main parameters

word_list <- read_csv("subject-1.csv") %>%
  pull(word) %>%
  unique(.) %>%
  tolower(.) # Create unique list of words to compare with data

vowel_list <- c("a","e","i","o","u")


# PART II: Outliers
# Create local folder to store the (eventual) outliers CSVs.

#setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/")
#dir.create("Cleanup")
setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/Cleanup")

# PART II A: Mislabeled Measurements
# Identify mislabeled tokens.

df_words <- df_50 %>%
  select(Filename, Subject, Vowel, Word)

mislabeled <- df_words %>%
  filter(!Word %in% word_list | 
           !Vowel %in% vowel_list)
  # Check for "words" which don't match the word list

overlabeled <- df_words %>%
  anti_join(mislabeled) %>% # only examine acceptable labels
  group_by(Subject, Word) %>%
  filter(n() != 2) # Return rows where word is labeled more than twice
                   # or missing label

corrections <- bind_rows(mislabeled, overlabeled) %>%
  arrange(Subject, Word) #%>%
  #write_csv("Corrections.csv")
  

# PART II B: NA Measurements
# Identify NA values within data. 
na_values <- df_50 %>% 
  filter(if_any(4:ncol(df_50), is.na)) %>% # Pick up the rows which have 
                                           # NA value(s) in any column 4+
  write_csv("NA_Values.csv") # Then save these rows in a csv

df_50_dropped <- df_50 %>%
  anti_join(na_values, by='Filename') %>%
  anti_join(mislabeled, by='Filename') %>%
  subset(select = -Word) %>%
  write_csv("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data/results_modified.csv")
  # Drop data with missing & mislabeled entries
  # Will examine that data separately
  
# PART II C: Normalization
# Create CSVs with outlier measurements. 

df_50_norm <- df_50_dropped %>% 
  group_by(Subject, Vowel) %>% # Calculations are based on the summaries of the
                               # vowels per speaker
  mutate(across(2:(ncol(df_50) - 3), # Replace the data in measure columns
                ~ c(scale(.)), .names = "Z_{col}")) 
                               # Take the entry in each column and feed into
                               # scale function, then output a list value, and 
                               # NOT A MATRIX!

z_score <- 2.5 # Value for outlier detection, can raise/lower as needed

pitch_outliers <- df_50_norm %>%
  filter(abs(Z_F0)>=z_score) %>% #pick up rows with abnormal z-score
  select(Filename, Subject, Vowel, F0, Z_F0) %>% #save only categorical & F0 column
  write_csv("Pitch_Outliers.csv") # And all data in a CSV file

formant_outliers <- df_50_norm%>%
  filter(if_any(Z_F1_50:Z_F4, ~ abs(.) >= z_score)) %>% 
    # Pick up rows where any of the Formant values are abnormal
  select(Filename, Subject, Vowel, F1_50, Z_F1_50,
         F2_50, Z_F2_50, F3_50, Z_F3_50, F4, Z_F4) %>% 
            # Keep formant columns 
  write_csv("Formant_Outliers.csv")

duration_outliers <- df_50_norm %>%
  filter(abs(Z_Duration)>=z_score) %>%
  select(Filename, Subject, Vowel, Duration, Z_Duration) %>%
  write_csv("Duration_Outliers.csv")

