## The number of the tier we want to use for extracting.
tier_number = 2

## Where the input sound files and textgrids are.
directory$ = "C:\Users\conno\git_repos\spanish_vowel_corpus\audio\word_segmented\"

## Where you want the segmented sound files and textgrids to be stored.
outdir$ = "C:\Users\conno\git_repos\spanish_vowel_corpus\audio\vowel_segmented\"

## Extension for sound files
extension$ = ".wav"

clearinfo
Create Strings as file list... list 'directory$'*'extension$'
number_of_files = Get number of strings

for a from 1 to number_of_files
    select Strings list
    current_sound$ = Get string... 'a'
    Read from file... 'directory$''current_sound$'
    current_sound$ = selected$("Sound")
    Read from file... 'directory$''current_sound$'.TextGrid
    num_intervals = Get number of intervals: tier_number
    appendInfoLine: current_sound$ + " " + string$(num_intervals)
    current_filename$ = ""
    current_start = 0
    current_end = 0
    for interval_number from 1 to num_intervals
        select TextGrid 'current_sound$'
        label$ = Get label of interval... tier_number interval_number
        if length(label$) > 0
            ## Interval is labeled
            if length(current_filename$) == 0
                ## Previous interval was not labeled, so we're starting a new file
                current_start = Get starting point... tier_number interval_number
                current_filename$ = label$ + "_" + current_sound$
            else
                current_filename$ = label$ + "_" + current_sound$
            endif
        elsif length(current_filename$) > 0
            ## Interval is not labeled but the previous interval was,
            ## means it's time to write a file.
            current_end = Get starting point... tier_number interval_number
            select Sound 'current_sound$'
            Extract part... current_start current_end rectangular 1.0 False
            name$ = outdir$ + current_filename$
            Save as WAV file... 'name$'.wav
            select TextGrid 'current_sound$'
            Extract part... current_start current_end rectangular 1.0 False
            Save as text file... 'name$'.TextGrid
            current_filename$ = ""
        endif
    endfor
    select all
    minus Strings list
    Remove
endfor