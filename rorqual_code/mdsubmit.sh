#!/bin/bash

#SBATCH --account=ctb-simine
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=2
#SBATCH --nodes=1
#SBATCH --time=0-08:00
#SBATCH --job-name=graphene_MD
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err


module load StdEnv/2023  intel/2023.2.1  openmpi/4.1.5
module load lammps-omp/20230802


export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Starting at $(date)"
srun lmp -in nvt.lammps
srun lmp -in nve.lammps 
echo "Ending at $(date)"
