#!/bin/bash

set -e


L=80.0
structype=${PWD##*/}
nstrucs=$(ls ~/scratch/clean_bigMAC/${structype}/*.xyz | wc -l)

if [[ $structype == '40x40' ]]; then
	inds=($(seq 1 $nstrucs))
else
	inds=($(seq 0 $(( nstrucs - 1 ))))
fi

ln -f ~/scratch/sAMC_MD/python_scripts/chop_MAC.py 


for n in ${inds[@]}; do
	echo $n
	python chop_MAC.py $structype $n $L

	cd "sample-${n}/${L}"

	ln -f ~/scratch/sAMC_MD/md_submit_1job.sh
	sbatch --job-name="${structype}-${n}_MD"  md_submit_1job.sh

	cd -
done

