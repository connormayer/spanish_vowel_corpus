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

        for j in range(len(labels)):
            if words_list[j] != labels[j]:
                num = num+1

                print("Mismatch in " + tg_name)
                
                prev = "-" if j == 0 else words_list[j-1]
                nex = "-" if j == 0 else words_list[j+1]                
                
                csv_writer.writerow([tg_name, prev,
                                     labels[j], nex, words_list[j]])
                break # Issue may affect the remaining order, stop loop

print("Done")
print("Please correct {} errors".format(num))


'''

##PART I: Set Up Corrections
import os
import pandas as pd

from praatio import textgrid


os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
words_df = pd.read_csv("subject-1.csv")["word"].unique()
words_list = [word.lower() for word in words_df]
    # List of actual words

os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/Cleanup")
corrections = pd.read_csv("corrections.csv")["Word"].unique()
    # List of words that need corrections, flagged from "Outlier Detection.R"

misspelled = [word for word in corrections if word not in words_list]

replace_list = [['beca', 'peca'], #[incorrect word, replacement]
                ['fiso', 'viso'],
                ['para', 'vara'],
                ['paso', 'baso'],
                ['pata', 'bata'],
                ['pate', 'bate'],
                ['piso', 'viso'],
                ['puque', 'buque'],
                ['vaso', 'baso'],
                ['sacque', 'saque'],
                ['vata', 'bata'],
                ['vate', 'bate'],
                ['veta', 'beta'],
                ['vota', 'bota'],
                ['vote', 'bote'],
                ['boco', 'toco'],
                ['pato', 'vato'],
                ['beto', 'veto'],
                ['quiso', 'viso'],
                ['corro', 'coro'],
                ['bato', 'vato'],
                ['queto', 'veto'],
                ['peque', 'seque'],
                ['visa', 'pisa'],
                ['pique', 'pite'],
                ['pusa', 'tusa'],
                ['peta', 'beta'],
                ['basto', 'baso'],
                ['cucu', 'cuco'],
                ['pita', 'pica'],
                ['tuso', 'puso'],
                ['base', 'baso'],
                ['photo', 'voto'],
                ['tuza', 'tusa'],
                ['bete', 'vete'],
                ['bisa', 'pisa'],
                ['boto', 'voto'],
                ['deta', 'beta'],
                ['deto', 'veto'],
                ['maso', 'baso'],
                ['sako', 'saco'],
                ['Seque', 'seque'],
                ['curra', 'cura'],
                ['foto', 'voto']
                ]



##PART II: Updating the TextGrids

os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/unsegmented")
filenames = os.listdir()
textgrid_list = [entry for entry in filenames if entry.endswith("d")]
    # List of all TextGrid files

for file in textgrid_list:
    print("Examining " + file)
    changes_made = False # Boolean marker to activate save process,
                         # resets for each TextGrid
    
    curr_grid = textgrid.openTextgrid(file,
                                 includeEmptyIntervals=False)
        # Imports TextGrid info for current subject
    
    words_tier = curr_grid.getTier('words')
    labels = [entry.label for entry in words_tier.entries]
        # List of word labels to examine for misspellings

    for word_pair in replace_list: 
        index_list = words_tier.find(word_pair[0])
            # Check if common mislabel exists in this TextGrid

        for i in index_list: # Loop over all occurances of misspelling
            instance = words_tier.entries[i] # Retrieve word interval information

            words_tier.insertEntry((instance[0], instance[1], word_pair[1]),
                                   # Preserve boundaries, fix label
                                 collisionMode='replace', # Replace entry with correction
                                 collisionReportingMode='silence')
            changes_made = True # Textgrid needs to be saved

    if changes_made == True:
        curr_grid.save(file, format="long_textgrid", includeBlankSpaces=True)
        # Save corrections, avoid overwriting correct files.

print('done')
'''










