#!/bin/bash

L=80.0
#structype=${PWD##*/}

if [[ $# != 1 ]]; then
	echo 'Must specify AMC ensemble!'
	exit 1
fi

structype=$1
cd "$structype"

nstrucs=$(ls ~/scratch/clean_bigMAC/${structype}/*.xyz | wc -l)

if [[ $structype == '40x40' ]]; then
	inds=($(seq 1 $nstrucs))
else
	inds=($(seq 0 $(( nstrucs - 1 ))))
fi

if [ ! -d vdos_npys_${L}_avgd/ ]; then
	mkdir vdos_npys_${L}_avgd/
fi

for n in ${inds[@]}; do
	cp sample-${n}/${L}/vdos-${n}.npy vdos_npys_${L}_avgd/
done

tar -czvf vdos_npys_${L}_avgd.tar.gz vdos_npys_${L}_avgd/
