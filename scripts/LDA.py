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
df=pd.read_csv("results_modified.csv")



##import data for model
X_Values=df.drop(["Filename", "Subject", "Vowel"], 1)
    #use acoustic measurements only
Y_Values=df["Vowel"]



##Visualizations for Normality
Titles=list(X_Values.columns)
    #create list for plot titles from pd df column names

#Histogram
FigureH, AxesH = plt.subplots(2, 3, figsize=(10,6))
    #initialize the figure & subplots for histogram
    #six independent variables - 2 rows 3 columns

for i in range(2): #iterate over rows
    for j in range(3): #iterate over columns
        k = 3*i+j
            #iterate through the dataframe/list, each row contains three cols
            # so after each row, 3 indices further into iterable
        plt.hist(X_Values.iloc[:,k]) #create histogram
        plt.sca(ax = AxesH[i,j]) #place in subplot
        AxesH[i,j].set_title(Titles[k]) #corresponding title since col names
FigureH.suptitle('Histogram', fontsize=16, fontweight='bold') #title fig
plt.tight_layout()

#QQ plots; same process as above
FigureQQ, AxesQQ = plt.subplots(2, 3, figsize=(10,6))

for i in range(2):
    for j in range(3):
        k = 3*i+j
        sm.qqplot(X_Values.iloc[:,k], ax = AxesQQ[i,j])
            #qqplot has subplot axes included in command
        AxesQQ[i,j].set_title(Titles[k])

FigureQQ.suptitle('QQ Plots', fontsize=16, fontweight='bold')
plt.tight_layout()

#plt.show() #display all plots 



##Model Training
kFold=RepeatedStratifiedKFold(n_splits=10, #num of k-folds
                           n_repeats=10) #num of repeats of 10-folds
    #define evaluation method (type of cross validation)

Model=[LinearDiscriminantAnalysis(),
       QuadraticDiscriminantAnalysis()] #define model types


for i in Model:
    Scores=cross_val_score(i, #model
                       X_Values, 
                       Y_Values,
                       cv=kFold, #cross validation splitting strategy
                       n_jobs=-1) #jobs use all processors
    print('mean accuracy of %.3f with standard %s model'
          % (np.mean(Scores), str(i))) #summarize result from model
breakpoint()

QDA=QuadraticDiscriminantAnalysis()
QDA.fit(X_Values, Y_Values)
    #train the model to implement it



##D Prime
Y_Predict=QDA.predict(X_Values)
    #use the model to predict classes, for use in dPrime calculation

Vowel_Class=pd.DataFrame({'Predicted':Y_Predict,
                          'Actual':Y_Values})
    #create datafram with class labels only

Vowel_List=Y_Values.unique().tolist()
    #creat list of vowels for use in pairwise calculations

n=len(Vowel_List)
pairs=[]

for i in range(n): 
    for j in range(i+1,n): #pair each vowel with the ones below
        pairs.append([Vowel_List[i],Vowel_List[j]])
            #generate list of pairs

Vowel_Class_Pairs=[Vowel_Class[Vowel_Class["Actual"].isin(list)]
                   for list in pairs] #create list of dfs with each pair

p=len(Vowel_Class_Pairs)
dPrime=np.zeros(p)
    #initialize storage of dPrime values, on efor each pair

for k in range(p):
    Current_Pair=Vowel_Class_Pairs[k] #iterate through the pairs
    m=len(Current_Pair)

    Total_Differents=0 #values used in dPrime
    Total_Sames=0

    Hits=0
    Alarms=0 
    
    for i in range(m): 
        for j in range(i+1,m): #compare each entry to the ones below
            if Current_Pair.iloc[i,0]!=Current_Pair.iloc[j,0]:
                    #given different vowels
                if Current_Pair.iloc[i,1]!=Current_Pair.iloc[j,1]:
                    #does the model recognize the difference
                    Hits+= 1
                Total_Differents+=1
                #regardless, count total different pairwise comparisons
            else:
                #the vowels are the same
                if Current_Pair.iloc[i,1]!=Current_Pair.iloc[j,1]:
                    #does the model assume they are different
                    Alarms+= 1
                Total_Sames+=1
                #regardless, count total same pairwise comparisons
    dPrime[k]=stats.norm.ppf(Hits/Total_Differents)-stats.norm.ppf(Alarms/Total_Sames)
    #calculate the dPrime Value and store

for i in range(p):
    print('The dPrime value of %s is %.3f'
          % (str(pair[i]), dPrime[i])) #summarize results








