#!/bin/bash
#SBATCH --account=def-simine
#SBATCH --time=0-06:00
#SBATCH --mem=500M
#SBATCH --output=slurm_avg.out
#SBATCH --error=slurm_avg.err


python just_average_vdos_npys.py tempdot6
