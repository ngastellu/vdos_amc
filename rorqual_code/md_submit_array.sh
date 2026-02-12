#!/bin/bash
#SBATCH --account=def-simine
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
#SBATCH --nodes=1
#SBATCH --array=0-19
#SBATCH --time=0-02:00
#SBATCH --output=slurm-%a.out
#SBATCH --error=slurm-%a.err


module load StdEnv/2023  intel/2023.2.1  openmpi/4.1.5
module load lammps-omp/20230802


export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK


rdir="80.0/subsample-${SLURM_ARRAY_TASK_ID}"

cd "$rdir"

ln ~/scratch/graphene_MD_obc/lammps_files/C_2010.tersoff

ln  ~/scratch/graphene_MD_obc/lammps_files/nve.lammps 
ln  ~/scratch/graphene_MD_obc/lammps_files/nvt.lammps  
ln  ~/scratch/graphene_MD_obc/python_scripts/write_data_file_size_test.py

python write_data_file_size_test.py 50

echo "Starting NVT at $(date)"
srun lmp -in nvt.lammps 
echo "Ending NVT at $(date)"

mv log.lammps log_nvt.lammps

echo "Starting NVE at $(date)"
srun lmp -in nve.lammps 
echo "Ending NVE at $(date)"

mv log.lammps log_nve.lammps
