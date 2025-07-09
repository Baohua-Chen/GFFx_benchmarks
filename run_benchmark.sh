#/bin/bash

## index
test_index(){
    parallel -j 1 "/usr/bin/time -v ./gffutils_cli.py create -f -m drop {}.gff 2> index/{}.index.log" ::: ps dm hs at
    parallel -j 1 "/usr/bin/time -v ../target/release/gffx index -i {1}.gff -a {2} 2> index/{1}.index.log" ::: ps dm hs at :::: product gene gene gene
}


test_extract(){
    dataset=$1
    outputdir=extract/${dataset}
    seq -w 100 | parallel -j 10 "i={}; shuf -n 100000 ${dataset}.gff.fts > ${outputdir}/input_{}.txt"
    ./benchmark_per_input.sh extract "../target/release/gffx extract -i ${dataset}.gff -t 1 -F "
    ./benchmark_per_input.sh extract "./gffutils_cli.py fetch ${dataset}.gff.db "
    ./benchmark_per_input.sh extract "gffread -F ${dataset}.gff --ids "
    ./benchmark_per_input.sh extract "./bcbio_extract.py ${dataset}.gff "
    ./benchmark_per_input.sh extract "agat_sp_filter_feature_from_keep_list.pl --gff ${dataset}.gff --config agat_config.yaml --keep_list "
}

test_intersect(){
    dataset=$1
    outputdir=intersect_st/${dataset}
    seq -w 100 | parallel -j 10 "i={}; bedtools random -l 20000 -n 100000 -g ${dataset}.fa.fai > ${outputdir}/input_{}.txt"
    ./benchmark.sh intersect "../target/release/gffx intersect -t 1 -i ${dataset}.gff --bed "
    ./benchmark.sh intersect "./gffutils_cli.py region ${dataset}.gff.db "
    ./benchmark.sh intersect "./agat_intersect.sh ${dataset}.gff "
    ./benchmark.sh intersect "bedtools intersect -a ${dataset}.gff -b "
    ./benchmark.sh intersect "./bcbio_intersect.py ${dataset}.gff "
    ./benchmark.sh intersect "./gffread_intersect.sh ${dataset}.gff "
}


test_index
for dataset in at dm
do
    test_extract $dataset
    test_intersect $dataset
done
