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


# Set directories
in_path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/word_segmented"
os.chdir(in_path)

out_path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/spectrograms/"


if os.path.isdir(out_path):
    shutil.rmtree(out_path)
os.mkdir(out_path)



results = process_corpus(corpus_path = in_path,
                         entry_classes=['words', 'vowels'],
                         target_tier='vowels', target_labels='[aeiou]',
                         min_duration=0.02,
                         min_max_formant=3000, max_max_formant=7000,
                         nstep=20, n_formants=5,
                         time_step=0.002)
print("Processed Corpus")

track_dicts = []
for track in results:
    # Save winner dataframe
    df = track.to_df(which = "winner").to_pandas()
    rows = len(df)
    midpoint = rows // 2

    file = df["file_name"][0]
    #sound = pm.Sound(os.path.join(in_path,file+".wav"))

    curr_dict = {}
    curr_dict.update({
        "Filename": file,
        "Subject": df["file_name"][0].split("_")[0],
        "Gender": df["file_name"][0].split("_")[1],
        "Vowel": df["label"][0],
        "Word": df["file_name"][0].split("_")[2],
        "F0": np.mean(track.sound.to_pitch().selected_array["frequency"])
        #np.mean(track.sound.to_pitch(pitch_ceiling = 300).selected_array["frequency"])
        })
    #to_pitch_ac()
    #pitch ceiling for m=200/f=250

    for i in range(1, 4):
        fx_df = df["F{}".format(i)]
        curr_dict.update({
            "F{}_{}".format(i, x):
            fx_df.iloc[np.percentile(range(rows),
                                     x, method = "nearest")]
            for x in range(10,100,10)
            })
    curr_dict.update({
        "F4": df["F4"].iloc[midpoint],
        "Duration": track.sound.duration
        })
    track_dicts.append(curr_dict)

    # Spectrogram Plot
    track.spectrograms()
    curr_plt = plt.gcf()
    curr_plt.suptitle(file, y=0.95, fontsize=16)
    curr_plt.supxlabel("Time (s)", y=0.04)
    curr_plt.supylabel("Frequency (Hz)", x = 0.05)
    curr_plt.savefig(out_path+file+'.png')
    plt.close()
    print(file+" finished")


data = pd.DataFrame(track_dicts)
breakpoint()


                                                                                     





'''

    
    #file_df = results[0].to_df(which = "all").to_pandas()
    #file_df = file_df[["F1", "F2", "F3", "F4", "max_formant", "time"]]
    #itvl = m.floor(file_df.shape[0]/10)

    #for i in range(10):
        #pd.DataFrame({'':[]})

subj14_m_    _saque_0.TextGrid
subj14_m_    _saque_0.wav

subj19_f_quite_  _saca_261.TextGrid
subj19_f_quite_  _saca_261.wav


'''
