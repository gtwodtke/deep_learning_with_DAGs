# Deep Learning with DAG: Replication Files

This repository contains the replication files for the paper "Deep Learning with DAG".

## Directory Structure

1. [Folder: blau_duncan_1967: ](#folder-blau_duncan_1967)
   Contains scripts for results in Section 5.1.
2. [Folder: zhou_2019: ](#folder-zhou_2019)
   Contains scripts for results in Section 5.2.
3. [Folder: MCEs: ](#folder-mces)
   Contains scripts for results in Appendix A.

---

### Folder: `blau_duncan_1967`
Contains scripts for results in Section 5.1.

- `DS1_1962_ssv_txt`: Original data from Blau and Duncan (1967) and our reanalysis. [Download here](https://scholar.harvard.edu/files/xzhou/files/zhou2019_college_replication.zip).
- `blau_duncan_1967_clean.py`: Cleans and converts data to CSV format.
- `blau_duncan_1967.py`: Processes data, trains models, and estimates point estimates.

#### Subfolder: `bootstrap`
Scripts for bootstrapping to generate confidence intervals.

- `blau_bootstrap.py`: Generates and processes bootstrap samples, trains models, and estimates point estimates in parallel.
- `init_blau_bootstrap.py`: Initiates `blau_bootstrap.py`.
- `blau_bootstrap.sbatch`: Slurm script for running `init_blau_bootstrap.py` on high performance computing cluster (HPC).
- `standardization.py`: Standardizes all computed results.
- `sum_blau_bootstrap_<ATE_XY/ATE_UY/NDENIE>.py`: Computes and plots 90% confidence intervals and point estimates on the average total effect of X on Y/ average total effect of U on Y/ natural direct and indirect effects of X on Y mediated by U.
- `plot_blau_bootstrap_<ATE_XY/ATE_UY/NDENIE>.py`: Plots point estimates and 90% confidence interval on the average total effect of X on Y/ average total effect of U on Y/ natural direct and indirect effects of X on Y mediated by U.

#### Subfolder: `sensitivity`
Scripts for sensitive analysis on the average total effect of U on Y.

- `blau_duncan_1967_sensitivity.py`: Processes data, trains models, and estimates point estimates on the average total effects of U on Y with sensitivity analysis
- `plot_blau_duncan_ATE_UY_sens.py`: Plots point estimates under sensitive analysis.

---

### Folder: `zhou_2019`
Contains scripts for results in Section 5.2.

- `nlsy79_samples.RData`: Original data for Zhou (2019) and our reanalysis. [Download here](https://scholar.harvard.edu/files/xzhou/files/zhou2019_college_replication.zip).
- `zhou_2019_clean.R`: Cleans and converts data to CSV format.
- `zhou_2019.py`: Processes data, trains models, and estimates point estimates.

#### Subfolder: `bootstrap`
Scripts for bootstrapping to generate confidence intervals.

- `zhou_bootstrap.py`: Generates and processes bootstrap samples, trains models, and estimates point estimates in parallel.
- `init_zhou_bootstrap.py`: Initiates `zhou_bootstrap.py`.
- `zhou_bootstrap.sbatch`: Slurm script for running `init_zhou_bootstrap.py` on HPC.
- `sum_zhou_bootstrap.py`: Computes 90% confidence intervals.

---

### Folder: `MCEs`
Contains scripts for results in Appendix A.

- `MCE.sbatch`: Slurm script for initiating relevant Python scripts on HPC.

#### Subfolders: `MCE_1`, `MCE_2`, `MCE_3`
Scripts for Monte Carlo experiments testing the performance of cGNF.

- `MCE_<1/2/3>.py`: Generates and processes Monte Carlo samples, trains models, and estimates point estimates in parallel.
- `init_MCE_<1/2/3>.py`: Initiates `MCE_<1/2/3>.py`.
- `sum_MCE_<1/2/3>.py`: Computes summary statistics.
- `plot_MCE_<1/2/3>.py`: Plots summary statistics.
- `est_<ATE/NDENIE/PSE>.py`: Calculates true values of the average total effects/ natural direct and indirect effects/ path-specific effects.

#### Subfolders: `Hyperparameter_1`, `Hyperparameter_2`
Scripts for testing the robustness of cGNF to variations in architecture and hyper-parameter settings.

- `Hyperparameters_<1/2>_<a, .., e>.py`: Produces Monte Carlo samples.
- `init_hyperparameters_<1/2>.py`: Initiates respective hyperparameter scripts.
- `sum_hyperparameters_<1/2>.py`: Computes summary statistics.
- `plot_hyperparameters_<1/2>.py`: Plots summary statistics.

#### Subfolders: `CI_Coverage`
Scripts for testing the confidence interval coverage rate of cGNF.

- `MCE_bootstrap.py`: Generates and processes bootstrap samples based on Monte Carlo samples, trains models, and estimates point estimates in parallel.
- `bootstrap_for_MCE.py`: Initiates `MCE_bootstrap.py`.
- `MCE_for_bootstrap.py`: Generates Monte Carlo samples.
- `template_sbatch.sh`: Slurm script for running `bootstrap_for_MCE.py` on HPC.
- `submit_jobs.sh`: Initiates `template_sbatch.sh` on HPC.
- `sum_MCE_bootstrap.py`: Computes 90% confidence intervals.
- `plot_MCE_bootstrap.py`: Plots 90% confidence intervals.
