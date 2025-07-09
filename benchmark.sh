#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <module> <cmd...>"
    exit 1
fi

module=$1
shift
cmd="$@"

raw_tool=$(echo "$cmd" | awk '{print $1}')
tool=$(basename "$raw_tool" | sed 's/-/_/g')

if [[ "$cmd" =~ ([A-Za-z0-9_]+)\.gff ]]; then
    dataset="${BASH_REMATCH[1]}"
else
    echo "Error: cmd must contain a .gff file with format like NAME.gff"
    exit 1
fi

outdir="${module}/${dataset}/${tool}"
mkdir -p "$outdir"

export cmd
export outdir
export module
export dataset

seq -w 1 100 | parallel -j 1 '
    i={}
    infile="${module}/${dataset}/input_${i}.txt"
    logfile="${outdir}/run_${i}.log"
    fullcmd="$cmd $infile > /dev/null 2> /dev/null"
    /usr/bin/time -v bash -c "$fullcmd" 2> "$logfile"
'
