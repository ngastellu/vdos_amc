#!/bin/bash
#SBATCH --account=ctb-simine
#SBATCH --time=0-10:00
#SBATCH --array=0-217
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=40G
#SBATCH --output=slurm_vdos_mpi-%a.out
#SBATCH --error=slurm_vdos_mpi-%a.err

module --force purge 
module load StdEnv/2023
module load python/3.13.2 scipy-stack/2025a
module load mpi4py

rundir="sample-${SLURM_ARRAY_TASK_ID}"
cd "$rundir"

ln -s ../get_vdos_mpi.py .
ln -s ../gather_mpi_vdos.py .

if [ ! -d 'mpi_vdos' ]; then
	mkdir 'mpi_vdos'
fi

srun python get_vdos_mpi.py
python gather_mpi_vdos.py
