#!/bin/bash

# inspiration - http://debuirebrian.blogspot.com/2010/06/converting-dicom-images-to-jpeg-in.html

# find all files in all subdirectories with dcm extension
# and put it into list
file_list=$(fd --extension dcm)

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
    dcmj2pnm -d -v -im +oj +Jq 90 +Wi 1 $file $trimmed.jpg

    dcm2json $file | python ./json-process.py > $trimmed.json
done

# THIS COULD BE REFACTORED, BUT I'M LAZY :(

# create folder for jpegs if it not exists
if [ -d img ] ; then
    echo "Folder already exists, continue..."
else
    mkdir img
fi

# find all jpegs and put it in folder
file_list=$(fd --extension jpg)

for file in $file_list ; do
    mv $file img
done

# create folder for json files
if [ -d JSON ] ; then
    echo "Folder already exists, continue..."
else
    mkdir JSON
fi

# find all jsons and put it in folder
file_list=$(fd --extension json)

for file in $file_list ; do
    mv $file JSON
done

python json-to-csv.py
rm -rf JSON
