#!/bin/bash
# debug line
#trap 'echo "# $BASH_COMMAND";read' DEBUG

# inspiration - http://debuirebrian.blogspot.com/2010/06/converting-dicom-images-to-jpeg-in.html

# Progress bar - https://github.com/fearside/ProgressBar/

# 1. Create ProgressBar function
# 1.1 Input is currentState($1) and totalState($2)
function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line

printf "\rProgress : [${_fill// /#}${_empty// /-}] ${_progress}%%"

}

# find all files in all subdirectories with dcm extension
# and put it into list

printf "Finding DICOM files in directory/subdirectories... "
file_list=$(fd --extension dcm)

printf "done.\n"
# initialize counter
number=1

# number of iterations for progress bar
_end=$(echo "$file_list" | wc -l)

printf '\nConverting DICOM files...\n'

# iterate over this list and convert each file
for file in $file_list ; do

    # trim extension
    trimmed=$(basename $file .dcm)

    # "-d"     - debug
    # "-v"     - verbose
    # "-im"    - print image details
    # "+oj"    - write JPEG
    # "+Jq 90" - compression quality (actually, this is default value)
    # "+Wi 1"  - window number(no idea, what this means)

    #dcmj2pnm -d -v -im +oj +Jq 90 +Wi 1 $file $trimmed.jpg
    dcmj2pnm +oj +Jq 90 +Wi 1 $file $trimmed.jpg

    # convert file into json and parse needed data from it
    dcm2json $file | python ./json-process.py > $trimmed.json

    # draw progress bar
    ProgressBar ${number} ${_end}
    # increment counter for progress bar
    number=$[$number+1]
done

printf '\nCreating folders... '
printf 'done.\n'

# create necessary folder, if they didn't exist
for dir in \
        "img" \
        "JSON"
do
    if [ -d "$dir" ]; then
        echo "${dir} folder already exists, continue..."
    else
        mkdir $dir
    fi
done

printf '\nMoving stuff to folders... '
printf 'done.\n'

# find all jpegs and put it in folder
jpg_list=$(fd --extension jpg)

# find all jsons and put it in folder
json_list=$(fd --extension json)

for file in $jpg_list ; do
    mv $file img
done

for file in $json_list ; do
    mv $file JSON
done

printf '\nCreating csv... '
printf 'done.\n'

python json-to-csv.py
rm -rf JSON

printf '\nFinished!\n'
