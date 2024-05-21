# PART I: SET UP & IMPORTING DATA
import os
import shutil
import pandas as pd


repo = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"
csv_path = os.path.join(repo, "Cleanup",
                            "formant_outliers.csv")
audio_path = os.path.join(repo, "audio",
                          "vowel_segmented")

spec_path = os.path.join(repo, "spectrograms")
fof_path = os.path.join(repo, "Cleanup",
                         "formant_outlier_files")

folders = ["pos", "neg", "mix"]
move_paths = [os.path.join(fof_path, folder) for folder in folders]

df = pd.read_csv(csv_path)


#'''
# PART II: MOVE FILES
def move_files(filename, move_path):
    filetypes = [".TextGrid", ".wav", ".png"]
    type_paths = [audio_path, audio_path, spec_path] # corresponding path
    n = len(type_paths)

    for i in range(n):
        file_full = filename + filetypes[i]
        source = os.path.join(type_paths[i], file_full)
        dest = os.path.join(move_path, file_full)
        shutil.move(source, dest)

pos_list = []
neg_list = []
mix_list = []

for index, row in df.iterrows():
    filename = df["Filename"][index]
    row_dict = row.to_dict()

    z_scores = row[["Z_F1_50", "Z_F2_50", "Z_F3_50", "Z_F4"]]
    pos_z = [x for x in z_scores if x>=2.5]
    neg_z = [x for x in z_scores if x<=-2.5]
    
    if not neg_z:
        pos_list.append(row_dict)
        move_path = move_paths[0]
    elif not pos_z:
        neg_list.append(row_dict)
        move_path = move_paths[1]
    else:
        mix_list.append(row_dict)
        move_path = move_paths[2]

    move_files(filename, move_path)
    
pd.DataFrame(pos_list).to_csv(os.path.join(move_paths[0],
                                           "0pos_formant_outliers.csv"),
                              index = False)
pd.DataFrame(neg_list).to_csv(os.path.join(move_paths[1],
                                           "0neg_formant_outliers.csv"),
                              index = False)
pd.DataFrame(mix_list).to_csv(os.path.join(move_paths[2],
                                           "0mix_formant_outliers.csv"),
                              index = False)

'''
# Part III: MOVE BACK

for move_path in move_paths:
    filenames = [name for name in os.listdir(move_path) if not name.endswith(".csv")]
    for file in filenames:
        source = os.path.join(move_path, file)
        if file.endswith("g"):
            dest = os.path.join(spec_path, file)
        else:
            dest = os.path.join(audio_path, file)
            
        shutil.move(source, dest)

#'''

breakpoint()
