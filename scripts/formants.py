import os
import shutil

from fasttrackpy import process_audio_file, \
    process_directory, \
    process_audio_textgrid,\
    process_corpus

import matplotlib.pyplot as plt
import math as m


# Set directories
in_path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/word_segmented/"
os.chdir(in_path)

out_path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/spectrograms/"


if os.path.isdir(out_path):
    shutil.rmtree(out_path)
os.mkdir(out_path)


# word_segmented file names
files = os.listdir()
files_list = list(set([file.split(".")[0] for file in files if not ""]))
#temp_list = files_list[:5]


temp_list = ["subj41_f_cuco_98"]
for file in temp_list:
    #print(file)
    audio_name = file+".wav"
    tg_name = file+".TextGrid"
    results = process_audio_textgrid(audio_path = os.path.join(in_path, audio_name),
                           textgrid_path = os.path.join(in_path, tg_name),
                           entry_classes=['words', 'vowels'],
                           target_tier='vowels', target_labels='[aeiou]',
                           min_duration=0.02, min_max_formant=3000,
                           max_max_formant=7000, nstep=20,
                           n_formants=5)
    breakpoint()
    
    #file_df = results[0].to_df(which = "all").to_pandas()
    #file_df = file_df[["F1", "F2", "F3", "F4", "max_formant", "time"]]
    #itvl = m.floor(file_df.shape[0]/10)

    #for i in range(10):
        #pd.DataFrame({'':[]})


    if results:
        results[0].spectrograms()
        curr_plt = plt.gcf()
        curr_plt.suptitle(file, y=0.95, fontsize=16)
        curr_plt.supxlabel("Time (s)", y=0.04)
        curr_plt.supylabel("Frequency (Hz)", x = 0.05)
        curr_plt.savefig(out_path+file+'.png')
        plt.close()

        results[0].winner.spectrogram()
        curr_win = plt.gcf()
        curr_win.suptitle(file+"_winner", y=0.95, fontsize=16)
        curr_win.savefig(out_path+file+'_win.png')
        plt.close()

    else:
        print("results for {} is empty".format(file))




'''


process_corpus(corpus_path = path, entry_classes=['Words', 'Vowels'],
               target_tier='Words', target_labels='[AEIOU]',
               min_duration=0.05,
               min_max_formant=4000, max_max_formant=7000,
               nstep=20, n_formants=4,
               window_length=0.025, time_step=0.002,
               pre_emphasis_from=50, smoother=Smoother(),
               loss_fun=Loss(), agg_fun=Agg())
'''
