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



##import data for model
x_values = df.drop(["Filename", "Subject", "Vowel"], 1)
    # Drop data that isn't acoustic measurements.

y_values = df["Vowel"]


'''
##Visualizations for Normality
titles = list(x_values.columns)
    # Create list from pd df column names to use as plot titles.

#Histogram
figure_hist, axes_hist  =  plt.subplots(2, 3, figsize = (10,6))
    # Initialize the figure & subplots for histogram with six independent
    # variables - 2 rows 3 columns.

#for row in range(2):
    for col in range(3):
        k  =  3*row+col
            # Iterate through the dataframe/list, each row contains three cols
            # so after each row, 3 indices further into iterable.
        plt.hist(x_values.iloc[:,k]) # Create histogram
        plt.sca(ax  =  axes_hist[row,col]) # Place in subplot
        axes_hist[row,col].set_title(titles[k])

figure_hist.suptitle('Histogram', fontsize = 16, fontweight = 'bold') # Title fig
plt.tight_layout()

#QQ plots; same process as above
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

breakpoint()

##Model Training
k_fold = RepeatedStratifiedKFold(n_splits = 10, # num of k-folds
                               n_repeats = 10 # num of repeats of 10-folds
                               ) 
    # Define evaluation method (type of cross validation) for model.

models = [LinearDiscriminantAnalysis(),
       QuadraticDiscriminantAnalysis()
       ]
    # Define model types


for model_type in models:
    Scores = cross_val_score(model_type,
                             x_values,
                             y_values,
                             cv = k_fold, # Cross validation splitting strategy
                             n_jobs = -1 # Jobs use all processors
                             )
    print('mean accuracy of %.3f with standard %s model'
          % (np.mean(Scores), str(model_type))
          )
    # Summarize result from model.


##D Prime Function
def d_prime(pair):
    # Takes as input a two-column dataframe of vowel pairs
    # and returns the d prime score for those pairs

    m=len(pair)

    total_differents=0 #values used in dPrime
    total_sames=0
    hits=0
    alarms=0 
    
    for i in range(m): 
        for j in range(i+1,m): #compare each entry to the ones below
            actual_1, predicted_1 = pair.iloc[i,0], pair.iloc[i,1]
            actual_2, predicted_2 = pair.iloc[j,0], pair.iloc[j,1]

            if actual_1 != actual_2:
                    #given different vowels
                if predicted_1 != predicted_2:
                    #does the model recognize the difference
                    hits += 1
                total_differents +=1
                #regardless, count total different pairwise comparisons
            else:
                #the vowels are the same
                if predicted_1 != predicted_2:
                    #does the model assume they are different
                    alarms += 1
                total_sames += 1
                #regardless, count total same pairwise comparisons
    return stats.norm.ppf(hits/total_differents)-stats.norm.ppf(alarms/total_sames)
    #calculate the dPrime Value and store
'''

def d_prime(pair):
    m=len(pair)

    total_differents=0 
    total_sames=0

    hits=0
    alarms=0 
    
    for i in range(m): 
        for j in range(i+1,m):
            if pair.iloc[i,0] != pair.iloc[j,0]:
                if pair.iloc[i,1] != pair.iloc[j,1]:
                    hits += 1
                total_differents +=1
            else:
                if pair.iloc[i,1] != pair.iloc[j,1]:
                    alarms += 1
                total_sames += 1
    return stats.norm.ppf(hits/total_differents)-stats.norm.ppf(alarms/total_sames)


##Different Models

x_values_f123d = x_values[['F1_50','F2_50','F3_50', 'Duration']]
x_values_f123 = x_values[['F1_50','F2_50','F3_50']]
x_values_f12d = x_values[['F1_50','F2_50','Duration']]
x_values_f12 = x_values[['F1_50','F2_50']] # partition the x_values

x_values_list = [x_values, x_values_f123d, x_values_f123, x_values_f12d, x_values_f12]
    # list of all groups of x values, including those for full model
l=len(x_values_list)

full = QuadraticDiscriminantAnalysis()
f123d = QuadraticDiscriminantAnalysis()
f123 = QuadraticDiscriminantAnalysis()
f12d = QuadraticDiscriminantAnalysis()
f12 = QuadraticDiscriminantAnalysis() # initialize qda models based on x_values

models_list = [full, f123d, f123, f12d, f12] # sort into list

fit_list = [models_list[i].fit(x_values_list[i], y_values) for i in range(l)]
    # fit the models

score_list = [fit_list[i].score(x_values_list[i], y_values) for i in range(l)]
    # score the models

predict_list = [fit_list[i].predict(x_values_list[i]) for i in range(l)]
    # predict vowels for the models


y_pd_comp_list = [pd.DataFrame({'Predicted': predict_list[i],
                          'Actual': y_values}
                           ) for i in range(l)]
    # create data frame with predicted and actual vowel classes for comparison


## Vowels & Pairs
vowel_list = y_values.unique().tolist()
    # Create list of vowels for use in pairwise calculations.

n = len(vowel_list)
pairs = []


for i in range(n): 
    for j in range(i+1,n):
        pairs.append(
            [vowel_list[i],vowel_list[j]]
            )

v = len(pairs)

vowel_class_pairs = [[y_pd_comp_list[i][y_pd_comp_list[i]["Actual"].isin(list)]
                      for list in pairs] # Create list of dfs with each pair
                     for i in range(l) # for each one of the models
                     ]

l = 1
v = 1

breakpoint()

dprime_df=pd.DataFrame()

for i in range(l):
    current_df = pd.DataFrame({'Model': [str(x_values_list[i].columns.values.tolist())
                                         for _ in range(v)],
                               'Accuracy': [score_list[i] for _ in range(v)],
                               'Vowels': pairs,
                               'dPrime Values': [d_prime(pair)
                                                 for pair in vowel_class_pairs[i][0]]})
    pd.concat([dprime_df, current_df])




'''
p = len(vowel_class_pairs)


pd.DataFrame({'Model':[str(x_values_list[0].columns.values.tolist())
                                         for _ in range(p)],
                                'Accuracy': [score_list[i] for _ in range(p)],
                                'Vowels': pairs,
                                'dPrime Values': [d_prime(pair)
                                                  for pair in vowel_class_pairs[i]]})

dprime_df=pd.DataFrame()

for i in range(l):
    current_df = pd.DataFrame({'Model':[str(x_values_list[i].columns.values.tolist())
                                         for _ in range(p)],
                                'Accuracy': [score_list[i] for _ in range(p)],
                                'Vowels': pairs,
                                'dPrime Values': [d_prime(pair)
                                                  for pair in vowel_class_pairs[i]]})
    
    





full_d_prime_values=[d_prime(vowel_class_pairs[k]) for k in range(p)]


full_scores = pd.DataFrame({'Model':['Full' for i in range(p)],
                            'Accuracy': [score_list for i in range(p)],
                            'Vowels': pairs,
                            'dPrime Values': full_d_prime_values})


vowel_class_pairs_fifty = [vowel_class_fifty[vowel_class_fifty["Actual"].isin(list)]
                   for list in pairs] # Create list of dfs with each pair

d_prime_values_fifty=[d_prime(vowel_class_pairs_fifty[k]) for k in range(p)]


'''

breakpoint()
