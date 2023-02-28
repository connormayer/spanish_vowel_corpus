#PART I: SET UP & IMPORTING DATA
#update working directory, using exported folder/files from R code
import os
os.chdir("/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/Cleanup")

import pandas as pd #package to work with data frames
import shutil #package to move files


#import csv's (exported from R) containing names of files to be moved,
    # convert to set for uniqueness, iterable
#list all single outlier types for iteration
NA_Values=set(pd.read_csv("NA_Values.csv")["Filename"])

Single_Outliers=[set(pd.read_csv("Pitch_Outliers.csv")["Filename"]),
                 set(pd.read_csv("Formant_Outliers.csv")["Filename"]),
                 set(pd.read_csv("Duration_Outliers.csv")["Filename"])]


#PART II: CHECK FOR DUPLICATES & CREATE INTERSECTION SETS
#confirm no intersection between NA and each X_Outliers,
    # unlikely since NA's relocated in R
for i in range(len(Single_Outliers)):
    if len(NA_Values.intersection(Single_Outliers[i]))==0:
        print("NA_Values and Outliers["+str(i)+"] are distinct")
    else:
        print("NA_Values and Outliers["+str(i)+"] overlap")


#create set with shared elements between all three outlier sets 
Triple_Outliers=Single_Outliers[0].intersection(Single_Outliers[1],
                                            Single_Outliers[2])


#if intersection exists, remove filenames from Single_Outliers,
    # so only in this new set and won't try to move file name twice
if Triple_Outliers==set():
    print("No triple intersection")
else:
    for filename in Triple_Outliers:
        Single_Outliers[0].discard(filename)
        Single_Outliers[1].discard(filename)
        Single_Outliers[2].discard(filename)
    print("Triple intersection set created")


#initialize sets for pairwise intersections,
    # check that intersection is non-empty, then remove as above
Double_Outliers=[set()]*3 #maximum 3 intersections
k=0 #index for double outliers, update as non-empty sets found

for i in range(len(Single_Outliers)):
    for j in range(i+1, len(Single_Outliers)):
        #compute intersection
        Current_Intersection=Single_Outliers[i].intersection(Single_Outliers[j])
        if Current_Intersection==set():
            print("Outliers["+str(i)+
                  "] and Outliers["+str(j)+"] are distinct") #empty, move on
        else:
            Double_Outliers[k]=Current_Intersection #save non-empty set in list
            for filename in Double_Outliers[k]:
                Single_Outliers[0].discard(filename)
                Single_Outliers[1].discard(filename)
                Single_Outliers[2].discard(filename)
            print("Outliers["+str(i)+
                  "] and Outliers["+str(j)+"] set created")
            k=k+1 

Double_Outliers.remove(set()) #remove any unassigned list entries


#PART III: CREATE FILE EXTENSIONS
#create list of all Outlier Sets, add file names to each entry in set
All_Outliers=[NA_Values]+Single_Outliers+Double_Outliers+[Triple_Outliers]
total=len(All_Outliers)

Extensions=[".wav",".TextGrid"] #want to move both audio and Praat files
All_Files=[[]]*total #initialize sets to store filenames with extensions

for k in range(total):
    All_Files[k]=[i+j for i in All_Outliers[k] for j in Extensions]
    #str concatenate both extensions to end of file names


#PART IV: MOVING THE FILES
#create the pathnames of files to move, folder to move to, then move each
Source_Path="/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/word_segmented/"
Outlier_Folders=["NA_Values/",
                 "Pitch_Outliers/", "Formant_Outliers/", "Duration_Outliers/",
                 "Triple_Outliers/", "Pitch_Formant_Outliers/", "Formant_Duration_Outliers/"]
Destination_Path=[""]*total
Partial_Path="/Users/meganlwe/Documents/GitHub/spanish_vowel_corpus/audio/"


for i in range(total):
    Destination_Path[i]=Partial_Path+Outlier_Folders[i]
    os.mkdir(Destination_Path[i])

for i in range(total):
    for j in All_Files[i]:
        Source= Source_Path+j
        Destination=Destination_Path[i]+j
        shutil.move(Source, Destination)
    





print("All files moved")




