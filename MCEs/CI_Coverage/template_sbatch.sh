#!/bin/bash

#SBATCH --job-name=test_JOBNAME
#SBATCH --account=ssd
#SBATCH --time=36:00:00
#SBATCH --partition=ssd
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --exclusive
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jessezhou1@rcc.uchicago.edu

module load parallel
module load python/anaconda-2022.05
source activate

cd /scratch/midway3/jessezhou1/
conda activate /scratch/midway3/jessezhou1/myenv
cd /project/wodtke/cGNF_python_code

srun="srun --exclusive -N1 -n1 --cpus-per-task $SLURM_CPUS_PER_TASK"
parallel="parallel --delay 0.2 -j $SLURM_NNODES --joblog runtask_${SLURM_JOB_ID}.log --resume"

export SLURM_OBJECT=SLURMOBJECT

$parallel "$srun python bootstrap_for_MCE.py {1} $SLURM_OBJECT > output_${SLURM_JOB_NAME}.{1}.log" ::: {1..5}
