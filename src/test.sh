#!/bin/sh

filename="api_test.txt"


while read -r line
do
    $line

done < "$filename"
