#!/usr/bin/env bash

gff_file="$1"
bed_file="$2"

while read -r chr start end _; do
    gffread "$gff_file" -r "${chr}:${start}-${end}" -o -
done < "$bed_file"
