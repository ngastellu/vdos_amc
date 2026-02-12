#!/bin/bash

set -e


L=80.0
seconds_per_subsample=90
extra_margin=10

structype=${PWD##*/}
nstrucs=$(ls -d sample-* | wc -l)


if [[ $structype == '40x40' ]]; then
	inds=($(seq 1 $nstrucs))
else
	inds=($(seq 0 $(( nstrucs - 1 ))))
fi

for i in ${inds[@]}; do
	run_dir="sample-${i}/80.0"
	cd $run_dir

	nb_subsamples=$(ls -d subsample-* | wc -l)
	serial_time=$(( extra_margin + seconds_per_subsample * nb_subsamples / 60 ))

	ln -sf  ~/scratch/sAMC_MD/submit_vdos_mpi_1job.sh

	sbatch --time=${serial_time} submit_vdos_mpi_1job.sh ${nb_subsamples}

	cd -
done



