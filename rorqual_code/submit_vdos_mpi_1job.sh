#!/bin/bash
#SBATCH --account=def-simine
#SBATCH --time=0-01:00
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=40G
#SBATCH --output=slurm_vdos_mpi.out
#SBATCH --error=slurm_vdos_mpi.err

module --force purge 
module load StdEnv/2023
module load python/3.13.2 scipy-stack/2025a
module load mpi4py

L=80.0
nb_subsamples=$(ls -d ${L}/subsample-* | wc -l)
vdos_script='get_vdos_mpi.py'
run_type='neglect-edge'

#for i in $(seq 0 $(( $nb_subsamples - 1))) ; do
for i in $(seq 1 $(( $nb_subsamples - 1))) ; do

	echo -e "\n--------------- subsample $i ---------------"

	rundir="${L}/subsample-${i}"
	cd "$rundir"

	ln -sf ~/scratch/graphene_MD_obc/python_scripts/${vdos_script} .
	ln -sf ~/scratch/graphene_MD_obc/python_scripts/gather_mpi_vdos.py .

	if [ ! -d 'mpi_vdos' ]; then
		mkdir 'mpi_vdos'
	fi

	dumpfile='dump_nve-50.lammpstrj'
	start_eq=120000
	end=600000
	step=50
	start_file=100000
	step_file=50

	srun python $vdos_script $dumpfile $start_eq $end $step $start_file $step_file
	python gather_mpi_vdos.py $run_type

	cd -
done

python ~/scratch/graphene_MD_obc/python_scripts/average_sample_vdos.py $L $run_type
