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

setwd(file.path(path, "histograms"))
for (subj in subj_list){
  mf_df %>%
    filter(Subject == subj) %>%
      ggplot(aes(x=Max_Formant), color = Vowel) +
      geom_histogram(bins=8, aes(y = after_stat(density))) +
      geom_density(lwd = .75, linetype = 1, color = "red") +
      facet_grid(Vowel ~ .) +
      theme_bw() +
      theme(panel.background = element_rect(fill = "white")) + 
      labs(title = sprintf("Count of Max Formants for %s", str_to_title(subj)),
           x = "Max Formant Measurement",
           y = "Density")
  
  ggsave(sprintf("%s_histogram.png", subj), width = 4, height = 5, units = "in")
}

mf_df %>% 
  group_by(Gender,Subject) %>% 
  summarize(Mean = mean(Max_Formant), 
            Median = median(Max_Formant))

