# PART I: SET UP & IMPORTING DATA
import os
import shutil
import pandas as pd

repo = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"
formant_path = os.path.join(repo, "Cleanup",
                            "formant_outliers.csv")
audio_path = os.path.join(repo, "audio",
                          "vowel_segmented")

spec_path = os.path.join(repo, "spectrograms")
move_path = os.path.join(repo, "Cleanup",
                         "f_out_specs")

filenames = list(pd.read_csv(formant_path)["Filename"])
filetypes = [".TextGrid", ".wav", ".png"]
type_paths = [audio_path, audio_path, spec_path] # corresponding path
n = len(source_paths)

# PART II: MOVE FILES
for file in filenames:
    for i in range(n):
        file_full = file + filetypes[j]
        source = os.path.join(source_paths[j], file_full)
        dest = os.path.join(move_path, file_full)
        shutil.move(source, dest)

breakpoint()
