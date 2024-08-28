import os
import pandas as pd



# Initialize
repo = "/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus"

results = pd.read_csv(os.path.join(repo,
                                   "data",
                                   "ft_results.csv")
                      )

# Correct Pitch Outliers
pitch = pd.read_csv(os.path.join(repo,
                                 "Cleanup",
                                 "pitch_outliers_corrected.csv")
                    )
pitch = pitch.loc[pitch["Correction"] != "-"][["Filename",
                                               "Correction"]]

df = results.merge(pitch, on="Filename", how="left")
    # Add Pitch Correction Col
df["F0"] = df["Correction"].fillna(df["F0"])
    # Replace F0 with Correction values, if none, take original F0 val
df.drop(columns=["Correction"], inplace=True)
df = df.set_index('Filename')


# Correct Formant Outliers
form = pd.read_csv(os.path.join(repo,
                                "Cleanup",
                                "formant_outlier_files",
                                "formant_outliers_corrected.csv")
                   ).set_index('Filename')
form = form.drop(columns = ["Subject", "Gender", "Vowel", "Word",
                            "F0", "Duration"])

df.update(form)
df = df.reset_index()


# Save CSV
df.to_csv(os.path.join(repo,
                       "data",
                       "ft_results_corrected.csv"), index = False)


print("done")
breakpoint()
