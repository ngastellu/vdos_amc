#!/bin/bash

L=80.0
structype=${PWD##*/}
nstrucs=$(ls ~/scratch/clean_bigMAC/${structype}/*.xyz | wc -l)

if [[ $structype == '40x40' ]]; then
	inds=($(seq 1 $nstrucs))
else
	inds=($(seq 0 $(( nstrucs - 1 ))))
fi

if [ ! -d vdos_npys_${L}_subsamples/ ]; then
	mkdir vdos_npys_${L}_subsamples/
fi

for n in ${inds[@]}; do
	mkdir vdos_npys_${L}_subsamples/sample-${n}/
	cp sample-${n}/${L}/subsample-*/vdos*.npy vdos_npys_${L}_subsamples/sample-${n}/
done

tar -czvf vdos_npys_${L}_subsamples.tar.gz vdos_npys_${L}_subsamples/
