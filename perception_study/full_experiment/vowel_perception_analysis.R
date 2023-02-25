library(lme4)
library(tidyverse)

# Read in experimental results
setwd("C:/Users/conno/git_repos/spanish_vowel_corpus/perception_study/full_experiment")
#setwd("E:/git_repos/spanish_vowel_corpus/perception_study/full_experiment")

#Read read in the filenames of all files from the naming task
filenames <- list.files("data")

# Create tibbles to hold experimental data
task <- tibble()
test_run <- tibble()
consent <- tibble()
background <- tibble()
audio_check <- tibble()

# Read in each experimental data file, force reaction time to be numeric,
# and add it to our task tibble
for (filename in filenames) {
  result <- read_csv(paste("data/", filename, sep=""), show_col_types = FALSE) %>%
    filter(`Event Index` != "END OF FILE")
  if (str_detect(filename, '7e5k')) {
    consent <- rbind(consent, result)
  } else if (str_detect(filename, 'enic')) {
    background <- rbind(background, result)
  } else if (str_detect(filename, 'gkan')) {
    audio_check <- rbind(audio_check, result)
  } else if (str_detect(filename, '43kc')) {
    test_run <- rbind(test_run, result)
  } else{
    result <- result %>% mutate(as.numeric(`Reaction Time`))
    task <- rbind(task, result) 
  }
}

# Clean up column names
task <- task %>% 
  rename(ID = `Participant Private ID`,
         date = `UTC Date`,
         zone = `Zone Type`,
         response = Response,
         block = block,
         correct = Correct,
         RT = `Reaction Time`,
         trial = `Trial Number`,
         subject = subject,
         gender = gender,
         vowel = vowel,
         word = word, 
         group = group)

# Do some clever joining to provide NA values under response in cases where
# users didn't choose a vowel before the timer ran out. These cases won't 
# have a corresponding entry for 'response_button_text' but will have an
# entry for 'fixation'. We join the two using a full join, which populates
# missing variables with NA.
task_responses <- task %>%
  filter(zone == "response_button_text")
# 
# task_trials <- task %>%
#   filter(zone == "fixation")
# 
# task_responses <- task_responses %>%
#   select(ID, response, RT, trial, block, correct, filename)
# 
# task_trials <- task_trials %>%
#   select(ID, vowel, word, group, block, subject, gender, trial, filename)
# 
# task_full <- full_join(task_responses, task_trials, by=c("ID", "trial", "block", "filename"))

task_full <- task_responses %>%
  select(ID, response, RT, trial, block, correct, filename, vowel, word, group, subject, gender)

#Tidy up a few labeling errors in spreadsheet
task_full <- task_full %>%
  mutate(vowel = ifelse(vowel == 'ao', 'a', vowel)) %>%
  mutate(vowel = ifelse(vowel == 'oo', 'o', vowel)) %>%
  mutate(vowel = ifelse(vowel == 'io', 'i', vowel))

# mislabeled_row <- task_full %>% filter(filename == 'a_subj2_f_vara_85.wav' & block == 'quiet')
# mislabeled_row$vowel <- 'a'
# mislabeled_row$word <- 'vara'
# mislabeled_row$group <- '9-A'
# mislabeled_row$subject <- 'subj2'
# mislabeled_row$gender <- 'f'
# mislabeled_row$correct <- mislabeled_row$response == 'a'
# 
# task_full <- task_full %>%
#   rows_update(mislabeled_row, by = c("ID", "filename"))
# 
# mislabeled_row <- task_full %>% filter(filename == 'o_subj48_f_toco_162.wav' & block == 'noise')
# mislabeled_row$vowel <- 'o'
# mislabeled_row$word <- 'toco'
# mislabeled_row$group <- '7-A' 
# mislabeled_row$subject <- 'subj48'
# mislabeled_row$gender <- 'f'
# mislabeled_row$correct <- mislabeled_row$response == 'o'
# 
# task_full <- task_full %>%
#   rows_update(mislabeled_row, by = c("ID", "filename"))
# 
# mislabeled_row <- task_full %>% filter(filename == 'o_subj7_f_voto_241.wav' & block == 'noise')
# mislabeled_row$vowel <- 'o'
# mislabeled_row$word <- 'voto'
# mislabeled_row$group <- '7-A'
# mislabeled_row$subject <- 'subj7'
# mislabeled_row$gender <- 'f'
# mislabeled_row$correct <- mislabeled_row$response == 'o'

# task_full <- task_full %>%
#   rows_update(mislabeled_row, by = c("ID", "filename"))

# Create some plots

# Plot percent correct by block/vowel
task_full %>%
  group_by(vowel, block) %>%
  summarize(correct=mean(correct, na.rm=TRUE)) %>%
ggplot() +
  geom_bar(aes(x=vowel, y=correct, fill=block), position='dodge', stat = "identity") +
  ylim(0, 1)
ggsave('figures/percent_correct_by_block.png')

# Plot percent correct by gender/vowel
task_full %>%
  group_by(vowel, gender) %>%
  summarize(correct=mean(correct, na.rm=TRUE)) %>%
  ggplot() +
  geom_bar(aes(x=vowel, y=correct, fill=gender), position='dodge', stat = "identity") +
  ylim(0, 1)
ggsave('figures/percent_correct_by_gender.png')

# Plot confusion matrix broken down by block
task_full %>%
  group_by(vowel, block, response) %>%
  summarize(count = n()) %>%
ggplot(aes(vowel, response, fill=count)) +
  geom_tile() +
  geom_text(aes(label=count)) +
  scale_fill_gradient(trans='log', breaks=c(0, 2, 8, 32, 128, 512), low="white", high="darkblue") +
  facet_grid(~ block)
ggsave('figures/confusion_matrix.png')

# Plot histogram of individual token responses
task_full %>%
  group_by(filename) %>%
  summarise(correct = mean(correct)) %>%
ggplot(aes(x=correct)) + 
  geom_histogram()
ggsave('figures/token_histogram.png')

# create confusion matrix

task_full %>%
  group_by(vowel, response) %>%
  count() %>%
  pivot_wider(names_from=response, values_from=n) %>%
  write_csv('../confusion_matrix.csv')
