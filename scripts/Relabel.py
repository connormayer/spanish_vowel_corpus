import os

import pandas as pd
import csv

from praatio import textgrid


# Create list of dfs with word ordering
os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/subject_orderings")
csv_list = ["Subject-" + str(i+1) + ".csv" for i in range(81)]
df_list = [pd.read_csv(file)["word"] for file in csv_list]

# Create list of textgrid file names
os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/unsegmented")
tg_filenames = os.listdir()
tg_list = [entry for entry in tg_filenames if entry.endswith("d")]


corrections = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/Cleanup/corrections.csv"

num = 0 # Counter for number of corrections

# Write correction info into a CSV
with open(corrections,
          'a',
          newline = '') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Subject', 'Prev',
                         'Label', 'Next', 'Actual'])
    # Order: subject , last correct label, label that raised issue,
    #        what the next label should be, actual label for error       

    for i in range(81):
        words_list = [word.lower() for word in df_list[i]]

        tg_name = [name for name in tg_list
                   if name.startswith("subj"+str(i+1)+"_")][0]
            # Find the name of the subject since order may not match index
        grid = textgrid.openTextgrid(tg_name,
                                     includeEmptyIntervals=False)
        words_tier = grid.getTier('words')
        labels = [entry.label for entry in words_tier.entries]
        labels += ["-", "-", "-"]

        for j in range(len(words_list)):
            #print(words_list[j],labels[j])
            if words_list[j] != labels[j]: 
                num = num+1

                print("Mismatch in " + tg_name)
                prev = "-" if j == 0 else words_list[j-1]
                nex = "-" if j == len(words_list)-1 else words_list[j+1]                
                
                csv_writer.writerow([tg_name, prev,
                                     labels[j], nex, words_list[j]])
                break # Issue may affect the remaining order, stop loop
    
print("Done")
print("Please correct {} errors".format(num))









