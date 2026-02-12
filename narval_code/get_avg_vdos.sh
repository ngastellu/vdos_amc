#!/bin/bash

set -e 

if [[ $# != 1 ]]; then
	echo 'ERROR: need to specify ensemble'
	exit 1
fi


structype=$1
sample_dirs=($(ls -d "${structype}/"sample-*))

for sample_dir in ${sample_dirs[@]}; do
	echo -n "${sample_dir}... "
	cd "${sample_dir}/80.0"
	ln -sf ~/scratch/sAMC_MD/python_scripts/average_sample_vdos.py
	python average_sample_vdos.py
	echo 'Done!'
	cd -
done
