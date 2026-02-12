#!/bin/bash
#SBATCH --account=ctb-simine
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=2
#SBATCH --nodes=1
#SBATCH --time=0-02:00
#SBATCH --array=0-217
#SBATCH --job-name=MAC_MD
#SBATCH --output=slurm-%a.out
#SBATCH --error=slurm-%a.err


module load StdEnv/2023  intel/2023.2.1  openmpi/4.1.5
module load lammps-omp/20230802


export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK


rdir="sample-${SLURM_ARRAY_TASK_ID}"

if [ ! -d "$rdir" ]; then
	mkdir "$rdir"
	cp CH.airebo "$rdir"
fi

cd "$rdir"

#ln -s ../nve.lammps
ln -s ../nvt.lammps
#ln -s ../write_data_file.py .
ln -s ../truncate_MAC.py .

python truncate_MAC.py 'tempdot6' $SLURM_ARRAY_TASK_ID
python write_data_file.py $SLURM_ARRAY_TASK_ID

echo "Starting NVT at $(date)"
srun lmp -in nvt.lammps 
echo "Ending NVT at $(date)"

echo "Starting NVE at $(date)"
srun lmp -in nve.lammps 
echo "Ending NVE at $(date)"
