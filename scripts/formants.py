import os
import shutil

from fasttrackpy import process_audio_file, \
    process_directory, \
    process_audio_textgrid,\
    process_corpus
import parselmouth as pm

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import math as m

# If Empty Functions
def f123_value(df, num):
    name = "F{}".format(num)
    value = name in df.columns
    rows = len(df)
    
    if value:
        fx_df = df[name]
        add_dict = {
            "F{}_{}".format(num, x):
            fx_df.iloc[np.percentile(range(rows),
                                     x, method = "nearest")]
            for x in range(10,100,10)
            }
    else:
        add_dict = {"F{}_{}".format(num, x): None
                    for x in range(10,100,10)}
    return add_dict

def f4_value(df, point):
    value = "F4" in df.columns
    if value: 
        add_dict = {"F4": df["F4"].iloc[point]}
    else:
        add_dict = {"F4": None}
    return add_dict



# Set Directories
repo = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/"

in_path = os.path.join(repo, "audio", "vowel_segmented")
os.chdir(in_path)

spec_path = os.path.join(repo, "spectrograms")

'''
if os.path.isdir(spec_path):
    shutil.rmtree(spec_path)
os.mkdir(spec_path)
'''

fof_path = os.path.join(repo, "Cleanup",
                        "formant_outlier_files")


# Collect Formants from Corpus
def get_results(corpus_path, results_name,
                spec_path = False, data_path = False,
                hist_name = False, 
                min_max_formant = 3000, max_max_formant=7000):
    if not spec_path:
        spec_path = corpus_path
    if not data_path:
        data_path = os.path.join(repo, "data")
    # Run FastTrack calls
    results = process_corpus(corpus_path = corpus_path,
                         entry_classes=['words', 'vowels'],
                         target_tier='vowels', target_labels='[aeiou]',
                         min_duration=0,
                         min_max_formant=min_max_formant,
                         max_max_formant=max_max_formant,
                         nstep=20, n_formants=5,
                         time_step=0.002)
    print("Processed Corpus")

    # Extract Info and save to df
    result_dicts_list = []
    hist_dicts_list =[]
    m_ceil = 200
    f_ceil = 300
    for track in results:
        # Save winner dataframe
        df = track.to_df(which = "winner").to_pandas()
        
        rows = len(df)
        midpoint = rows // 2
        
        file = df["file_name"][0]
        file_split = file.split("_")
        vowel = file_split[0]
        subj = file_split[1]
        gender = file_split[2]
        print(file)
        pitch_ceiling = m_ceil if file.split("_")[2] == 'm' else f_ceil

        results_dict = {}
        results_dict.update({
            "Filename": file,
            "Subject": subj,
            "Gender": gender,
            "Vowel": vowel,
            "Word": file_split[3],
            "F0": np.mean(track.sound.to_pitch_ac(pitch_ceiling)
                          .selected_array["frequency"])
            })

        for i in range(1, 4):
            results_dict.update(f123_value(df, i))    

        results_dict.update(f4_value(df, midpoint))
        results_dict.update({"Duration": track.sound.duration})
        
        result_dicts_list.append(results_dict)
        '''
        # Spectrogram Plot
        track.spectrograms()
        curr_plt = plt.gcf()
        curr_plt.suptitle(file, y=0.95, fontsize=16)
        curr_plt.supxlabel("Time (s)", y=0.04)
        curr_plt.supylabel("Frequency (Hz)", x = 0.05)
        curr_plt.savefig(os.path.join(spec_path, file+'.png'))
        plt.close()
        '''
        if hist_name:
            hist_dict = {}
            hist_dict.update({"Subject": subj,
                              "Gender": gender,
                              "Vowel": vowel,
                              "Max_Formant": df["max_formant"][0]})
            hist_dicts_list.append(hist_dict)
        

    data = pd.DataFrame(result_dicts_list)
    data.to_csv(os.path.join(data_path, results_name), index = False)

    if hist_name:
        hist_data = pd.DataFrame(hist_dicts_list)
        hist_data.to_csv(os.path.join(data_path, hist_name), index = False)

        breakpoint()

# Whole Corpus
get_results(corpus_path= in_path,
            results_name = "ft_results.csv",
            hist_name = "max_formants.csv",
            spec_path = spec_path)
'''

# Pos/Neg Outliers
pos_max = 6000
neg_min = 4000

pos_path = os.path.join(fof_path, "pos")
neg_path = os.path.join(fof_path, "neg")
get_results(corpus_path = pos_path,
            results_name = "0pos_formant_outliers_corrections.csv",
            data_path = pos_path,
            max_max_formant = pos_max)

get_results(corpus_path = neg_path,
            results_name = "0neg_formant_outliers_corrections.csv",
            data_path = neg_path,
            min_max_formant = neg_min)
'''

print("done")
breakpoint()










