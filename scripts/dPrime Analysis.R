#install.packages("tidyverse")
library(tidyverse, warn.conflicts = FALSE)


# PART I: Importing Data
# Import the CSV (exported from Python) and pull vowel pairs and parameters. 

setwd("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
df <- read_csv("dprime.csv") # Import dPrime data

pairs <- unique(df[3]) # Create tibble of vowel pairs
num_pairs <- nrow(pairs)

params <- unique(df[1]) %>% 
  filter(str_detect(Model, ',', negate = TRUE)) # Create tibble of parameters
    

# PART II: Scoring
# Use data to compare accuracy & dPrime scores.

df_acc <- df %>% 
  filter(Vowels == as.character(pairs[1,1])) %>% # Model accuracy = across pairs
                                                 # so pick one pair
  select(Model, Accuracy) # Select model name & general accuracy score

df_acc_m <- rbind(slice_max(df_acc, Accuracy),
                  slice_min(df_acc, Accuracy)) # Return rows w max & min

df_group <- df %>% group_by(Vowels) # Create groups of Vowel Pairs

df_maxes <- df_group %>%
  slice_max(dPrime, n = 2) %>%
  arrange(desc(dPrime)) # Return the first n dPrime maxes for each pair


# PART III: Parameter Analysis
# Create plot of effect of individual parameters across vowel pairs. 

yes_df <- data.frame(Included=rep(TRUE, each = num_pairs))
  # Create tibble of TRUE values for each vowel pair
no_df <- data.frame(Included=rep(FALSE, each = num_pairs))
  #FALSE's

data = NULL # Initialize tibble
data_mean = NULL
for (x in 1:nrow(params)){
  curr_param <- as.character(params[x,1])
    # Pick parameter
  parameter_df <- data.frame(Parameter=rep(curr_param, each = num_pairs))
    # Create tibble of parameter name
  
  dfy <- df_group %>% 
    filter(str_detect(Model, curr_param)) %>%
    summarize(dPrime = mean(dPrime)) %>%
      # Compute the average dPrime score for all models trained with curr_param
    bind_cols(parameter_df, yes_df)
      # Store in tibble with TRUE cols
  
  dfy_mean <- dfy %>%
    summarise(dPrime = mean(dPrime)) %>%
    bind_cols(Parameter = curr_param, Included = "TRUE")
  
  dfn <- df_group %>% 
    filter(str_detect(Model, curr_param, negate = TRUE)) %>%
    summarize(dPrime = mean(dPrime)) %>%
      # All models trained WITHOUT curr_param
    bind_cols(parameter_df, no_df)
      # Store in tibble with FALSE cols
  
  dfn_mean <- dfn %>%
    summarise(dPrime = mean(dPrime)) %>%
    bind_cols(Parameter = curr_param, Included = "FALSE")
    
  data <- bind_rows(data, dfy, dfn)
    # Update tibble
  
  data_mean <- bind_rows(data_mean, dfy_mean, dfn_mean)
}

# Plot data:
data %>%
  ggplot(aes(x = Vowels,
             y = dPrime,
             color = Parameter,
             shape = Included))+
  geom_point()+
  guides(shape = guide_legend(reverse=TRUE))+
  scale_shape_manual(values = c(1,19))+ # Hollow & filled circles
  scale_colour_brewer(palette = "Set1") +
  labs(title = "Average dPrime Score",
       x = "Vowel Pairs",
       y = "dPrime")

data_mean %>%
  ggplot(aes(x = Parameter,
             y = dPrime,
             shape = Included))+
  geom_point(size=3)+
  guides(shape = guide_legend(reverse=TRUE))+
  scale_shape_manual(values = c(1,19))+ # Hollow & filled circles
  labs(title = "Average dPrime Scores Across Vowel Pairs",
       x = "Vowel Pairs",
       y = "dPrime")

