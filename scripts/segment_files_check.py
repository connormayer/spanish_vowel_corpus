import os
import re

import pandas as pd

def create_string_name(subject, word):
    regex_pattern = fr'{subject}_\w_{re.escape(word)}'
    return re.compile(regex_pattern)

path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/"
words_list = pd.read_csv(os.path.join(path, "audio", "subject_orderings",
                                      "subject-1.csv"))["word"].unique()
words_list = [word.lower() for word in words_list]

audio_files = os.listdir(os.path.join(path, "audio", "word_segmented"))

missing_subj = []
for subj in range(1, 82):
    subj_files = [file for file in audio_files
                  if file.startswith("subj{}_".format(subj))]
    if len(subj_files) != 160:
        missing_subj += ["subj{}".format(subj)]

missing_words = []

for subj in missing_subj:
    for word in words_list:
        string = create_string_name(subj, word)
        match_list = [file for file in audio_files if string.match(file)]

        found = len(match_list)
        if found<4:
            curr_dict = {
                "Subject": subj,
                "Word": word,
                "Count": 4-found}
            missing_words.append(curr_dict)

pd.DataFrame(missing_words).to_csv(os.path.join(path, "Cleanup",
                                                "missing_TG.csv"),
                                   index = False)

print("done")


