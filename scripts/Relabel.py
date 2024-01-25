##PAART I: Set Up Corrections
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











