#!/bin/bash
# ./download.sh url/messi.csv ./test

url_file=$1
if [ -z "$2" ]
then
    images_dir="."
else
    images_dir=$2
fi

while read line || [[ -n "$line" ]]; do
    file=${line##*/}
    file=${file%%\?*}
    echo downloading $line to $images_dir/$file
    curl -o file $line
done < "$url_file"
