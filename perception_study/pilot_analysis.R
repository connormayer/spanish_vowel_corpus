library(lme4)
library(tidyverse)

# Read in experimental results
setwd("C:/Users/conno/git_repos/spanish_vowel_corpus/perception_study")

#Read read in the filenames of all files from the naming task
filenames <- list.files("results_files")

# Create tibble to hold experimental data
task <- tibble()

# Read in each experimental data file, force reaction time to be numeric,
# and add it to our task tibble
for (filename in filenames) {
  result <- read_csv(paste("results_files/", filename, sep=""))
  result <- result %>% mutate(as.numeric(`Reaction Time`))
  task <- rbind(task, result)
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

task_trials <- task %>%
  filter(zone == "fixation")

task_responses <- task_responses %>%
  select(ID, response, RT, trial, block, correct, filename)

task_trials <- task_trials %>%
  select(ID, vowel, word, group, block, subject, gender, trial, filename)

task_full <- full_join(task_responses, task_trials, by=c("ID", "trial", "block", "filename"))

# Create some plots

# Plot percent correct by block/vowel
task_full %>%
  group_by(vowel, block) %>%
  summarize(correct=mean(correct, na.rm=TRUE)) %>%
ggplot() +
  geom_bar(aes(x=vowel, y=correct, fill=block), position='dodge', stat = "identity")

# Plot percent correct by gender/vowel
task_full %>%
  group_by(vowel, gender) %>%
  summarize(correct=mean(correct, na.rm=TRUE)) %>%
  ggplot() +
  geom_bar(aes(x=vowel, y=correct, fill=gender), position='dodge', stat = "identity")

# Plot confusion matrix broken down by block
task_full %>%
  group_by(vowel, block, response) %>%
  summarize(count = n()) %>%
ggplot(aes(vowel, response, fill=count)) +
  geom_tile() +
  geom_text(aes(label=count)) +
  facet_grid(~ block)

# Plot histogram of individual token responses
task_full %>%
  group_by(filename) %>%
  summarise(correct = mean(correct)) %>%
ggplot(aes(x=correct)) + 
  geom_histogram()
