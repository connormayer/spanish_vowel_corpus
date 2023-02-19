#PART I: Importing Data
#import the CSV (exported from Praat) and subset it

setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
#install.packages("tidyverse")
library(tidyverse, warn.conflicts = FALSE)

df<-read_csv("results.csv", 
             na=c("","NA", "--undefined--")) #data has missing entries
                                             #na sets all entries as NA values

df_50<-df %>%
  select(Filename, Subject, Vowel, F0, F1_50, F2_50, F3_50, F4, Duration)


#PART II: Outliers
#create local folders to store the (eventual) outliers CSVs
setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/")
dir.create("Cleanup")
setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/Cleanup")

##PART II A: NA Measurements
NA_Values<-df_50 %>% #using our refined data set
  filter(if_any(4:ncol(df_50), is.na)) %>% #pick up the rows which have 
                                           #a NA value in any column 4 & on
  write_csv("NA_Values.csv") #then save these rows in a csv


##PART II B: Normalization
df_50_norm<-df_50 %>%
  drop_na(4:ncol(df_50)) %>% #remove any NA-valued row, 
                             #since examining separately
  group_by(Subject, Vowel) %>% #calculations are based on the summaries of the 
                               #vowels per speaker
  mutate(across(2:(ncol(df_50) - 2), #replace the data in columns (minus group)
                ~ c(scale(.)))) #take the entry in each column and feed into
                                #scale function, then output a list value, and 
                                #NOT A MATRIX!

z_score<-2.5 #value for outlier detection, can raise/lower as needed

Pitch_Outliers<-df_50_norm %>%
  filter(abs(F0)>=z_score) %>% #pick up rows with abnormal z-score
  select(Filename, Subject, Vowel, F0) %>% #save only categorical & F0 column
  write_csv("Pitch_Outliers.csv") #and all data in a CSV file

Formant_Outliers<-df_50_norm%>%
  filter(if_any(F1_50:F4, ~ abs(.) >= z_score)) %>% 
    #pick up rows where any of the Formant values are abnormal
  select(!c(F0, Duration)) %>% #keep every column but Pitch & Duration
  write_csv("Formant_Outliers.csv")

Duration_Outliers<-df_50_norm %>%
  filter(abs(Duration)>=z_score) %>%
  select(Filename, Subject, Vowel, Duration) %>%
  write_csv("Duration_Outliers.csv")

