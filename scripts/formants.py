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

#import warnings
#warnings.filterwarnings("error")


# If Empty Functions
def f123_value(df, num):
    name = "F{}".format(num)
    value = name in df.columns
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





# Set directories
path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/"
in_path = os.path.join(path, "audio", "vowel_segmented")
os.chdir(in_path)

spec_path = os.path.join(path, "spectrograms")

if os.path.isdir(spec_path):
    shutil.rmtree(spec_path)
os.mkdir(spec_path)


# Collect Formants from Corpus
results = process_corpus(corpus_path = in_path,
                         entry_classes=['words', 'vowels'],
                         target_tier='vowels', target_labels='[aeiou]',
                         min_duration=0,
                         min_max_formant=3000, max_max_formant=7000,
                         nstep=20, n_formants=5,
                         time_step=0.002)
print("Processed Corpus")




# Extract Info and save to df
track_dicts = []
m_ceil = 200
f_ceil = 300
for track in results:
    # Save winner dataframe
    df = track.to_df(which = "winner").to_pandas()
    rows = len(df)
    midpoint = rows // 2
    
    file = df["file_name"][0]
    file_split = file.split("_")
    print(file)
    pitch_ceiling = m_ceil if file.split("_")[2] == 'm' else f_ceil

    curr_dict = {}
    curr_dict.update({
        "Filename": file,
        "Subject": file_split[1],
        "Gender": file_split[2],
        "Vowel": file_split[0],
        "Word": file_split[3],
        "F0": np.mean(track.sound.to_pitch_ac(pitch_ceiling)
                      .selected_array["frequency"])
        })

    for i in range(1, 4):
        curr_dict.update(f123_value(df, i))    

    curr_dict.update(f4_value(df, midpoint))
    curr_dict.update({"Duration": track.sound.duration})
    

    track_dicts.append(curr_dict)


    # Spectrogram Plot
    track.spectrograms()
    curr_plt = plt.gcf()
    curr_plt.suptitle(file, y=0.95, fontsize=16)
    curr_plt.supxlabel("Time (s)", y=0.04)
    curr_plt.supylabel("Frequency (Hz)", x = 0.05)
    curr_plt.savefig(os.path.join(spec_path, file+'.png'))
    plt.close()

data = pd.DataFrame(track_dicts)
data.to_csv(os.path.join(path, "data", "ft_results.csv"), index = False)







