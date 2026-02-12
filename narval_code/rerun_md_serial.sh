#!/bin/bash

set -e


L=80.0
structype=${PWD##*/}

istart=$1
iend=$2

echo "Submitting samples $istart to $iend (inclusive)."

inds=($(seq $istart $iend))

for n in ${inds[@]}; do
	echo $n

	if [ ! -d "sample-${n}/${L}" ]; then
		python chop_MAC.py $structype $n $L
	fi

	cd "sample-${n}/${L}"

	ln -f ~/scratch/sAMC_MD/md_submit_serial.sh

	sbatch --job-name="${structype}-${n}_MD"  md_submit_serial.sh

	cd -
done

