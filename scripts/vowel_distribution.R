#install.packages("tidyverse")
library(tidyverse, warn.conflicts = FALSE)
path <- "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"

# Importing Data 
setwd(file.path(path, "data"))
df <- read_csv("ft_results.csv") %>%
  select(Gender, Vowel, ends_with("_50"), F4) %>%
  group_by(Gender, Vowel)

#Compute Means and Standard Deviations
summ_stats <- df %>% 
  summarize(across(starts_with("F"), 
                   list(mean = mean, #drop.na
                        sd = sd),
                   .names = "{col}_{fn}"))

# Probabilistic Model
f_prob <- function(value, gender, vowel, formant){
  params <- summ_stats %>% 
    filter(Gender == gender, Vowel == vowel) %>%
    ungroup() %>%
    select(starts_with(formant))
  
  mu <- params %>% 
    pull(ends_with("mean"))
  
  sigma <- params %>% 
    pull(ends_with("sd")) 
 
  return(dnorm(value, mu, sigma)*100) 
}

f_prob(800, "m", "a", "F1") # example

# Histograms
mf_df <- read_csv("max_formants.csv")
subj_list <- mf_df %>% pull(Subject) %>% unique(.) 
subj_list = subj_list[1]
for (subj in subj_list){
  subj_df <- mf_df %>%
    filter(Subject == subj) %>%
    filter(Vowel == "a") %>%
    select(-Subject)
  
  subj_df %>%
    ggplot(aes(x="Max Formant")) +
    geom_histogram(color = "black", bins = 20, alpha = 0.7, stat="count") +
    #labs(title = ) +
    theme_minimal()
}

mf_df %>% group_by(Subject) %>% summarize(median(`Max Formant`))

