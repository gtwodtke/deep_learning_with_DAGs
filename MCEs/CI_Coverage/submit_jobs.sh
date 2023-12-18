#!/bin/bash

for n in {0..99}; do
    # Replace placeholders in the template script
    sed "s/JOBNAME/$n/g" template_sbatch.sh > temp_job_$n.sh
    sed -i "s/SLURMOBJECT/$n/g" temp_job_$n.sh

    # Submit the job
    sbatch temp_job_$n.sh
done
