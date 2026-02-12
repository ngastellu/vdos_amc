#!/bin/bash
#SBATCH --account=ctb-simine
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=2
#SBATCH --nodes=1
#SBATCH --time=0-06:00
#SBATCH --output=slurm_serial.out
#SBATCH --error=slurm_serial.err


module load StdEnv/2023  intel/2023.2.1  openmpi/4.1.5
module load lammps-omp/20230802

nb_subsamples=$(find . -maxdepth 1 -type d -name "subsample-*" | wc -l)

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK


inds=($(seq 0 $(( nb_subsamples - 1 ))))

for n in ${inds[@]}; do
	echo -e "\n----- Subsample $n -----"
	rdir="subsample-${n}"

	cd "$rdir"

	ln ~/scratch/sAMC_MD/lammps_files/C_2010.tersoff
	ln  ~/scratch/sAMC_MD/lammps_files/nve.lammps 
	ln  ~/scratch/sAMC_MD/lammps_files/nvt.lammps  

	ln  ~/scratch/sAMC_MD/python_scripts/write_data_file_size_test.py

	python write_data_file_size_test.py 50

	echo "Starting NVT at $(date)"
	srun lmp -in nvt.lammps 
	echo "Ending NVT at $(date)"

	mv log.lammps log_nvt.lammps

	echo "Starting NVE at $(date)"
	srun lmp -in nve.lammps 
	echo "Ending NVE at $(date)"

	mv log.lammps log_nve.lammps

	cd -
done
