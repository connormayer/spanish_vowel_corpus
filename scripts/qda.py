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

from more_itertools import powerset

import concurrent.futures

print("reading CSV...")

os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/data")
df = pd.read_csv("results_modified.csv")



## Import data for model
x_values = df.drop(["Filename", "Subject", "Vowel"], 1)
    # Drop data that isn't acoustic measurements.

y_values = df["Vowel"] # Vowel classes


## Define Mean Accuracy
def accuracy(model, n_splits = 10, n_repeats = 10):
    # Takes as input a model trained on x_values, y_values inported above
    # and returns the mean accuracy from the k-fold cross validation
    
    k_fold = RepeatedStratifiedKFold(n_splits=n_splits, # num of k-folds
                                     n_repeats=n_repeats
                                         # num of repeats of 10-folds
                                     )

    scores = cross_val_score(model,
                             x_values,
                             y_values,
                             cv = k_fold, # Cross validation splitting strategy
                             n_jobs = -1 # Jobs use all processors
                             )

    return np.mean(scores)


## D Prime Function
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


if __name__ == '__main__':

    ## Model Creation
    print("creating models...")
    
    params = set(x_values.columns) # Create unique set of all x_values

    combo_list = [list(i) for i in powerset(params)]
        #Create list of lists, inner list contains the combinations of x_values
    combo_list = combo_list[1:] # Ignore the empty set
    n = len(combo_list)

    x_values_list = [x_values[i] for i in combo_list]
        # Create list of dataframes using powerset combinations

    models_fit = [QuadraticDiscriminantAnalysis().fit(x, y_values) for x in x_values_list]
        # Fit a QDA model for each combination

    models_scores = [accuracy(model) for model in models_fit]
        # Score the model using the accuracy definition from above
        
    models_predict = [models_fit[i].predict(x_values_list[i]) for i in range(n)]
        # Predict vowel classes using each model
        # Generates a list of lists

    print("comparing scores...")

    y_df_comp_list = [pd.DataFrame({'Predicted': m_values,
                                    'Actual': y_values}
                                   ) for m_values in models_predict]
        # Create list of DataFrames containing Model's predicted class
        # and actual vowel for given measurements



    ## Vowels & Pairs
    vowel_list = y_values.unique().tolist()
        # Create list of vowels for use in pairwise calculations.
    v = len(vowel_list)
    
    pairs_list = []
    
    for i in range(v): 
        for j in range(i+1,v):
            pairs_list.append(
                [vowel_list[i],vowel_list[j]]
                )
            # List of pair-wise vowel comparisons
    p = len(pairs_list)

    vowel_class_pairs = [[y_df_comp_list[i][y_df_comp_list[i]
                                            ["Actual"].isin(pair)]
                          for pair in pairs_list] # Create list of dfs with each pair
                         for i in range(n) # for each one of the models
                         ]

    
    
    ## Results
    print("calculating dPrime...")

    
    dp_results = []
    for select in vowel_class_pairs:
        with concurrent.futures.ProcessPoolExecutor() as executor: # Parallelize
            dp_results += [list(executor.map(d_prime, select))]
                # Concat list of dPrime scores


    seperator = ','
    models_names = [seperator.join(model) for model in combo_list]
            # Create list of strings of parameters to identify model
    

    print("generating results CSV...")

    results_list = []

    for i in range(n):
        curr_df = pd.DataFrame({'Model':[models_names[i] for _ in range(p)],
                              'Accuracy': [models_scores[i] for _ in range(p)],
                              'Vowels': pairs_list,
                              'dPrime': dp_results[i]})
        results_list += [curr_df]
        # Create DataFrame with dprime scores and model info


    results_all = pd.concat(results_list,
                            axis=0,
                            ignore_index=True
                            ).to_csv('dprime.csv', index=False)
        # Export CSV
    
    print("results complete")
    
 


 








    
