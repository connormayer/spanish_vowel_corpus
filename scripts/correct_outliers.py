import os
import pandas as pd




path = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"

results = pd.read_csv(os.path.join(path,
                                   "data",
                                   "ft_results.csv"))
pitch = pd.read_csv(os.path.join(path,
                                 "Cleanup",
                                 "pitch_outliers_corrected.csv"))

pitch_fix = pitch.loc[pitch["Correction"] != "-"][["Filename",
                                                   "Correction"]]
df = results.merge(pitch_fix, on="Filename", how="left")
df["F0"] = df["Correction"].fillna(df["F0"])
df.drop(columns=["Correction"], inplace=True)

df.to_csv(os.path.join(path,
                       "data",
                       "ft_results_corrected.csv"))
breakpoint()
