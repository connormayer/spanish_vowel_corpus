import os

import numpy as np
import pandas as pd

from scipy.stats import multivariate_normal 

# Initialize
repo = '/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus'
data_path = os.path.join(repo, 'data')
cl_path = os.path.join(repo, 'Cleanup')
fof_path = os.path.join(cl_path, 'formant_outlier_files')


# Read Data and Outlier CSVs
df = pd.read_csv(os.path.join(data_path,
                              'ft_results.csv'))
df = df[['Filename','Subject', 'Vowel',
         'F1_50', 'F2_50', 'F3_50']]

out_df = pd.read_csv(os.path.join(cl_path,
                                  'formant_outliers.csv')
                     )[['Filename']]

df = df[~df.Filename.isin(out_df.Filename)] # only consider "good" measurements

        
# Calculate Vector Means and Covariance Matrix 
vals = {}
for subj_num in range(81):
    s_vals = {}
    subj_str = "".join(['subj', str(subj_num+1)])
    s_df = df[df['Subject'].isin([subj_str])]

    for vowel in ['a','e','i','o','u']:
        s_v_df = s_df[s_df['Vowel'].isin([vowel])]
        means = np.array([np.mean(s_v_df[[formant]])
                          for formant in ['F1_50', 'F2_50','F3_50']])
        cov = np.cov(np.transpose(s_v_df.drop(columns = ['Filename',
                                                         'Subject',
                                                         'Vowel'])))

        eigenvalues = np.linalg.eigvals(cov)
        if np.any(eigenvalues < 0):
            print("The matrix for {} vowel {} is not SPD".format(subj_str, vowel))

        v_vals = {'means': means, 'cov': cov}
        s_vals.update({vowel: v_vals})

    vals.update({subj_str: s_vals})


# Calculate Probability
min_max_formant = 3000
max_max_formant = 7000
ranges = {"pos": range(max_max_formant, 3500, -500),
          "neg": range(min_max_formant, 6500, 500)}
corrections = []
formant_ranges = []


for out_type in ["pos", "neg"]:
    out_type_path = os.path.join(fof_path, out_type)
    out_type_df = pd.read_csv(os.path.join(out_type_path,
                                           "0{}_formant_outliers.csv".format(
                                               out_type)))
    out_type_df = out_type_df.sort_values(by=['Subject', 'Vowel'])
    #po_out = pos_out[pos_out['Subject'].isin(['subj14'])]

    dfs_list = [pd.read_csv(os.path.join(out_type_path,
                                             "0{}_formant_outliers_{}.csv".format(out_type, x)
                                             )
                                ).set_index('Filename')
                    for x in ranges[out_type]]
    curr_subj = None
    curr_vowel = None

    for _, row in out_type_df.iterrows():
        file = row["Filename"]
        print(file)
        if curr_subj != row['Subject'] or curr_vowel != row['Vowel']:
            curr_subj = row['Subject']
            curr_vowel = row['Vowel']
            curr_mu = vals[curr_subj][curr_vowel]['means']
            curr_Sigma = vals[curr_subj][curr_vowel]['cov']
            dist = multivariate_normal(mean=curr_mu, cov=curr_Sigma)
   
        # pull up the new values
        df_formants = [np.array([df.loc[file]["F1_50"], df.loc[file]["F2_50"],
                           df.loc[file]["F3_50"]]) for df in dfs_list]

        # calculate probability based on speaker
        probs = [dist.pdf(formant) for formant in df_formants]
        
        # save correct prob
        df_index = probs.index(max(probs))

        if out_type == 'pos':
            f_r_dict = {'Filename': file, 'Min': min_max_formant,
                      'Max': ranges['pos'][df_index]}
        else:
            f_r_dict = {'Filename': file, 'Min': ranges['neg'][df_index],
                      'Max': max_max_formant}
                      
        formant_ranges += [f_r_dict]
        
        row_dict = {'Filename': file}
        row_dict.update(dfs_list[df_index].loc[file].to_dict())
        corrections += [row_dict]

corrections_df = pd.DataFrame(corrections)
corrections_df.to_csv(os.path.join(fof_path, "formant_outliers_corrected.csv"), index = False)

formant_ranges_df = pd.DataFrame(formant_ranges)
formant_ranges_df.to_csv(os.path.join(fof_path, "formant_ranges.csv"), index = False)


breakpoint()












