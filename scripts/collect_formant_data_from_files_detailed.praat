# This script goes through sound and TextGrid files in a directory,
# opens each pair of Sound and TextGrid, calculates the formant values
# at the midpoint of each labeled interval, and saves results to a text file.
# To make some other or additional analyses, you can modify the script
# yourself... it should be reasonably well commented! ;)
#
# This script is distributed under the GNU General Public License.
# Copyright 4.7.2003 Mietta Lennes

form Analyze formant values from labeled segments in files
	comment Directory of sound files
	text sound_directory C:\Users\conno\git_repos\spanish_vowel_corpus\audio\word_segmented\
	sentence Sound_file_extension .wav
	comment Directory of TextGrid files
	text textGrid_directory C:\Users\conno\git_repos\spanish_vowel_corpus\audio\word_segmented\
	sentence TextGrid_file_extension .TextGrid
	comment Full path of the resulting text file:
	text resultfile C:\Users\conno\git_repos\spanish_vowel_corpus\audio\results.csv
	comment Which tier has the vowels you want to analyze?
	sentence Tier vowels
	comment Formant analysis parameters
	positive Time_step 0.01
	integer Maximum_number_of_formants 5
	positive Maximum_formant_(Hz) 5500
	positive Window_length_(s) 0.025
	real Preemphasis_from_(Hz) 30
endform

# Here, you make a listing of all the sound files in a directory.
# The example gets file names ending with ".wav" from D:\tmp\

Create Strings as file list... list 'sound_directory$'*'sound_file_extension$'
numberOfFiles = Get number of strings

# Check if the result file exists:
if fileReadable (resultfile$)
	pause The result file 'resultfile$' already exists! Do you want to overwrite it?
	filedelete 'resultfile$'
endif

# Write a row with column titles to the result file:
# (remember to edit this if you add or change the analyses!)

titleline$ = "Filename,Subject,Gender,Vowel,Word,F0,F1_10,F1_20,F1_30,F1_40,F1_50,F1_60,F1_70,F1_80,F1_90,F2_10,F2_20,F2_30,F2_40,F2_50,F2_60,F2_70,F2_80,F2_90,F3_10,F3_20,F3_30,F3_40,F3_50,F3_60,F3_70,F3_80,F3_90,F4,Duration'newline$'"
fileappend "'resultfile$'" 'titleline$'

# Go through all the sound files, one by one:

for ifile to numberOfFiles
	filename$ = Get string... ifile
	# A sound file is opened from the listing:
	Read from file... 'sound_directory$''filename$'
	# Starting from here, you can add everything that should be 
	# repeated for every sound file that was opened:
	soundname$ = selected$ ("Sound", 1)
	hyp = index(soundname$, "_")
	subject$ = left$(soundname$, hyp - 1)
	gender$ = mid$(soundname$, hyp + 1, 1)

	To Formant (burg)... time_step maximum_number_of_formants maximum_formant window_length preemphasis_from

	select Sound 'soundname$'
	To Pitch... 0.01 75 600
	# Open a TextGrid by the same name:
	gridfile$ = "'textGrid_directory$''soundname$''textGrid_file_extension$'"
	if fileReadable (gridfile$)
		Read from file... 'gridfile$'
		# Find the tier number that has the label given in the form:
		call GetTier 'tier$' tier
		numberOfIntervals = Get number of intervals... tier
		# Pass through all intervals in the selected tier:
		for interval to numberOfIntervals
			label$ = Get label of interval... tier interval
			if label$ <> ""
				# if the interval has an unempty label, get its start and end:
				start = Get starting point... tier interval
				end = Get end point... tier interval
				midpoint = (start + end) / 2
				word_interval = Get interval at time: 1, midpoint
				word$ = Get label of interval... 1 word_interval

				# get the formant values at that interval
				select Formant 'soundname$'
				point10 = start + (end - start) * 0.1
				point20 = start + (end - start) * 0.2
				point30 = start + (end - start) * 0.3
				point40 = start + (end - start) * 0.4
				point50 = start + (end - start) * 0.5
				point60 = start + (end - start) * 0.6
				point70 = start + (end - start) * 0.7
				point80 = start + (end - start) * 0.8
				point90 = start + (end - start) * 0.9

				f1_10 = Get value at time... 1 point10 Hertz Linear
				f1_20 = Get value at time... 1 point20 Hertz Linear
				f1_30 = Get value at time... 1 point30 Hertz Linear
				f1_40 = Get value at time... 1 point40 Hertz Linear
				f1_50 = Get value at time... 1 point50 Hertz Linear
				f1_60 = Get value at time... 1 point60 Hertz Linear
				f1_70 = Get value at time... 1 point70 Hertz Linear
				f1_80 = Get value at time... 1 point80 Hertz Linear
				f1_90 = Get value at time... 1 point90 Hertz Linear

				f2_10 = Get value at time... 2 point10 Hertz Linear
				f2_20 = Get value at time... 2 point20 Hertz Linear
				f2_30 = Get value at time... 2 point30 Hertz Linear
				f2_40 = Get value at time... 2 point40 Hertz Linear
				f2_50 = Get value at time... 2 point50 Hertz Linear
				f2_60 = Get value at time... 2 point60 Hertz Linear
				f2_70 = Get value at time... 2 point70 Hertz Linear
				f2_80 = Get value at time... 2 point80 Hertz Linear
				f2_90 = Get value at time... 2 point90 Hertz Linear

				f3_10 = Get value at time... 3 point10 Hertz Linear
				f3_20 = Get value at time... 3 point20 Hertz Linear
				f3_30 = Get value at time... 3 point30 Hertz Linear
				f3_40 = Get value at time... 3 point40 Hertz Linear
				f3_50 = Get value at time... 3 point50 Hertz Linear
				f3_60 = Get value at time... 3 point60 Hertz Linear
				f3_70 = Get value at time... 3 point70 Hertz Linear
				f3_80 = Get value at time... 3 point80 Hertz Linear
				f3_90 = Get value at time... 3 point90 Hertz Linear

				f4 = Get value at time... 4 point50 Hertz Linear

				# Get duration
				duration = end - start

			    select Pitch 'soundname$'

			    f0 = Get value at time... midpoint Hertz Linear

				# Save result to text file:
				resultline$ = "'soundname$','subject$','gender$','label$','word$','f0','f1_10','f1_20','f1_30','f1_40','f1_50','f1_60','f1_70','f1_80','f1_90','f2_10','f2_20','f2_30','f2_40','f2_50','f2_60','f2_70','f2_80','f2_90','f3_10','f3_20','f3_30','f3_40','f3_50','f3_60','f3_70','f3_80','f3_90','f4','duration''newline$'"
				fileappend "'resultfile$'" 'resultline$'
				select TextGrid 'soundname$'
			endif
		endfor
		# Remove the TextGrid object from the object list
		select TextGrid 'soundname$'
		Remove
	endif
	# Remove the temporary objects from the object list
	select Sound 'soundname$'
	plus Formant 'soundname$'
	Remove
	select Strings list
	# and go on with the next sound file!
endfor

Remove


#-------------
# This procedure finds the number of a tier that has a given label.

procedure GetTier name$ variable$
        numberOfTiers = Get number of tiers
        itier = 1
        repeat
                tier$ = Get tier name... itier
                itier = itier + 1
        until tier$ = name$ or itier > numberOfTiers
        if tier$ <> name$
                'variable$' = 0
        else
                'variable$' = itier - 1
        endif

	if 'variable$' = 0
		exit The tier called 'name$' is missing from the file 'soundname$'!
	endif

endproc

