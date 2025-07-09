#!/usr/bin/bash

outputdir=$(echo $2 | sed 's#\(intersect_st/[a-z][a-z]\)/\(.\+\)#\1/agat_outputs/\2#g')
agat_sp_filter_record_by_coordinates.pl --gff $1 -c agat_config.yaml --tsv $2 -o $outputdir
