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

df = df[~df.Filename.isin(out_df)] # only consider "good" measurements

        
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
        s_vals.update({vowel: vs_vals})

    vals.update({subj_str: s_vals})

breakpoint()
'''

# Calculate Probability
pos_path = os.path.join(fof_path, "pos")
pos_out = pd.read_csv(os.path.join(pos_path,
                                   "0pos_formant_outliers.csv"))
pos_out = pos_out.sort_values(by=['Subject', 'Vowel'])
pos_out = pos_out[pos_out['Subject'].isin(['subj14'])]

pos_dfs = [pd.read_csv(os.path.join(pos_path,
                                    "0pos_formant_outliers_{}.csv".format(x)
                                    )
                       ).set_index('Filename')
           for x in range(7000, 4000, -500)]


curr_subj = None
curr_vowel = None
corrections = []

for _, row in pos_out.iterrows():
    file = row["Filename"]
    if curr_subj != row['Subject'] or curr_vowel != row['Vowel']:
        curr_subj = row['Subject']
        curr_vowel = row['Vowel']
        curr_mu = vals[curr_subj][curr_vowel]['means']
        curr_Sigma = vals[curr_subj][curr_vowel]['cov']
        dist = multivariate_normal(mean=curr_mu, cov=curr_Sigma)
        
    # pull up the new values
    df_formants = [np.array([df.loc[file]["F1_50"], df.loc[file]["F2_50"],
                       df.loc[file]["F3_50"], df.loc[file]["F4"]]) for df in pos_dfs]

    # calculate probability based on speaker
    probs = [dist.pdf(formant) for formant in df_formants]
    breakpoint()
    # save correct prob
    df_index = probs.index(max(probs))
    
    row_dict = {'Filename': file}
    row_dict.update(pos_dfs[df_index].loc[file].to_dict())
    corrections += [row_dict]

corrections_df = pd.DataFrame(corrections)
corrections_df.to_csv(os.path.join(fof_path, "corrections.csv"), index = False)

breakpoint()












