import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats
import matplotlib.pyplot as plt

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
df = pd.read_csv("results_modified.csv")

## Import data
x_values = df.drop(["Filename", "Subject", "Vowel"], 1)
    # Drop data that isn't acoustic measurements.

y_values = df["Vowel"]


'''
## Visualizations for Normality
titles = list(x_values.columns)
    # Create list from pd df column names to use as plot titles.

# Histogram
figure_hist, axes_hist  =  plt.subplots(2, 3, figsize = (10,6))
    # Initialize the figure & subplots for histogram with six independent
    # variables - 2 rows 3 columns.

for row in range(2):
    for col in range(3):
        k  =  3*row+col
            # Iterate through the dataframe/list, each row contains three cols
            # so after each row, 3 indices further into iterable.
        plt.hist(x_values.iloc[:,k]) # Create histogram
        plt.sca(ax  =  axes_hist[row,col]) # Place in subplot
        axes_hist[row,col].set_title(titles[k])

figure_hist.suptitle('Histogram', fontsize = 16, fontweight = 'bold') # Title fig
plt.tight_layout()

# QQ plots; same process as above
figure_qq, axes_qq  =  plt.subplots(2, 3, figsize = (10,6))

for row in range(2):
    for col in range(3):
        k  =  3*row+col
        sm.qqplot(x_values.iloc[:,k], ax  =  axes_qq[row,col])
            # qqplot has subplot axes included in command.
        axes_qq[row,col].set_title(titles[k])

figure_qq.suptitle('QQ Plots', fontsize = 16, fontweight = 'bold')
plt.tight_layout()

plt.show()

'''


## Define models
models_list = [LinearDiscriminantAnalysis(), QuadraticDiscriminantAnalysis()]

k_fold = RepeatedStratifiedKFold(n_splits=10, # num of k-folds
                                     n_repeats=10
                                         # num of repeats of 10-folds
                                     )

for model in models_list:
    model.fit(x_values, y_values)

    scores = cross_val_score(model,
                             x_values,
                             y_values,
                             cv = k_fold, # Cross validation splitting strategy
                             n_jobs = -1 # Jobs use all processors
                             )

    print(f'Total score for {model} is {np.mean(scores)}')
    



