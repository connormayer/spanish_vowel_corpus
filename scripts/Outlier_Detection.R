#install.packages("tidyverse")
library(tidyverse, warn.conflicts = FALSE)


# PART I: Importing Data
# Import the CSV (exported from Praat) and subset it. Create Vowel & Word lists
# for data clean up.

path <- "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"
setwd(file.path(path, "data"))
df <- read_csv("ft_results_corrected.csv", 
               na=c("","NA", "--undefined--")) # Data has missing entries
                                             # na sets all entries as NA values
df_50 <- df %>%
  select(Filename, Subject, Vowel, Word, F0, ends_with("_50"), F4, Duration)
  # Pick main parameters

sub_ord_path <- file.path(path, "audio", "subject_orderings")
word_list <- read_csv(file.path(sub_ord_path, "subject-1.csv")) %>%
  pull(word) %>%
  unique(.) %>%
  tolower(.) # Create unique list of words to compare with data

vowel_list <- c("a","e","i","o","u")


# PART II: Outliers
# Create local folder to store the (eventual) outliers CSVs.

#dir.create("Cleanup")
setwd(file.path(path, "Cleanup"))

# PART II A: Mislabeled Measurements
# Identify mislabeled tokens.

df_words <- df_50 %>%
  select(Filename, Subject, Vowel, Word)

mislabeled <- df_words %>%
  filter(!Word %in% word_list | 
           !Vowel %in% vowel_list) %>%
  arrange(Subject, Word) #%>%
  # write_csv("mislabeled.csv")
  # Check for "words" which don't match the word list
  

# PART II B: NA Measurements
# Identify NA values within data. 
na_values <- df_50 %>% 
  filter(if_any(4:ncol(df_50), is.na)) %>% # Pick up the rows which have 
                                           # NA value(s) in any column 4+
  write_csv("NA_values.csv") # Then save these rows in a csv

df_50_dropped <- df_50 %>%
  anti_join(na_values, by='Filename') %>%
  anti_join(mislabeled, by='Filename') %>%
  subset(select = -Word) %>%
  write_csv(file.path(path, 
                      "data", 
                      "ft_results_50.csv"))
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

# Pitch
pitch_outliers <- df_50_norm %>%
  filter(abs(Z_F0)>=z_score) %>% #pick up rows with abnormal z-score
  select(Filename, Subject, Vowel, F0, Z_F0) %>% #save only categorical & F0 column
  add_column("Correction" = 0)

pitch_outliers_corrected <- read_csv("pitch_outliers_corrected.csv") %>%
  filter(Correction %in% c("-", NA))
  
pitch_outliers %>% 
  anti_join(pitch_outliers_corrected, by='Filename') %>%  
  write_csv("pitch_outliers.csv") # And all data in a CSV file

# Formants
formant_outliers <- df_50_norm %>%
  filter(if_any(Z_F1_50:Z_F4, ~ abs(.) >= z_score)) %>% 
    # Pick up rows where any of the Formant values are abnormal
  select(Filename, Subject, Vowel, F1_50, Z_F1_50,
         F2_50, Z_F2_50, F3_50, Z_F3_50, F4, Z_F4) 
            # Keep formant columns  

formant_outliers_corrected <- read_csv("formant_outlier_files/formant_outliers_corrected.csv")

formant_outliers <- formant_outliers %>% 
  anti_join(formant_outliers_corrected, by='Filename') %>%  
  write_csv("formant_outliers.csv") # And all data in a CSV file

# Duration 
duration_outliers <- df_50_norm %>%
  filter(abs(Z_Duration)>=z_score) %>%
  select(Filename, Subject, Vowel, Duration, Z_Duration) %>%
  write_csv("duration_outliers.csv")

# Plots of Outliers
f_out_counts <- formant_outliers %>%
  select(-c(starts_with('F'), "Z_F4")) %>%
  pivot_longer(!c(Subject, Vowel), 
               names_to = "Formant", values_to = "Z") %>%
  mutate(Formant = str_replace(Formant, "Z_", ""),
         Subject = str_replace(Subject, "subj", "")) %>%
  filter(abs(Z) >= z_score) %>%
  group_by(Subject, Vowel, Formant) %>%
  summarize(Count = n()) %>%
  mutate(Subject = as.numeric(Subject)) %>%
  arrange(Subject)
  
f_out_counts %>%  
  ggplot(aes(x = Subject)) +
  geom_bar() +
  facet_grid(Formant ~ ., scales='free_x') +
  scale_x_continuous(breaks = round(seq(min(0), max(81), by = 10),0)) +
  labs(title = "Counts of Formant Outliers by Subject")

