#!/bin/bash
#SBATCH --account=ctb-simine
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=40G
#SBATCH --output=slurm_vdos_mpi.out
#SBATCH --error=slurm_vdos_mpi.err

module --force purge 
module load StdEnv/2023
module load python/3.13.2 scipy-stack/2025a
module load mpi4py

nb_subsamples=$1

for i in $(seq 0 $(( $nb_subsamples - 1))) ; do

	echo -e "\n--------------- subsample $i ---------------"

	rundir="subsample-${i}"
	cd "$rundir"

	ln -sf ~/scratch/sAMC_MD/python_scripts/get_vdos_mpi.py .
	ln -sf ~/scratch/sAMC_MD/python_scripts/gather_mpi_vdos.py .

	if [ ! -d 'mpi_vdos' ]; then
		mkdir 'mpi_vdos'
	fi

	dumpfile='dump_nve-50.lammpstrj'
	start_eq=120000
	end=600000
	step=50
	start_file=100000
	step_file=50

	srun python get_vdos_mpi.py $dumpfile $start_eq $end $step $start_file $step_file
	python gather_mpi_vdos.py 'pinned'

	cd -
done

ln -sf ~/scratch/sAMC_MD/python_scripts/average_sample_vdos.py
python average_sample_vdos.py
