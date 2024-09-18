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

- `blau_bootstrap.py`: Generates and processes bootstrap samples, trains models, and computes estimates in parallel.
- `init_blau_bootstrap.py`: Initiates `blau_bootstrap.py`.
- `blau_bootstrap.sbatch`: Slurm script for running `init_blau_bootstrap.py` on high performance computing cluster (HPC).
- `standardization.py`: Standardizes all computed results.
- `sum_blau_bootstrap_<ATE_XY/ATE_UY/NDENIE>.py`: Computes 90% confidence intervals on the average total effect of X on Y/ average total effect of U on Y/ natural direct and indirect effects of X on Y mediated by U.
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

- `zhou_bootstrap.py`: Generates and processes bootstrap samples, trains models, and computes estimates in parallel.
- `init_zhou_bootstrap.py`: Initiates `zhou_bootstrap.py`.
- `zhou_bootstrap.sbatch`: Slurm script for running `init_zhou_bootstrap.py` on HPC.
- `sum_zhou_bootstrap.py`: Computes 90% confidence intervals.

---

### Folder: `MCEs`
Contains scripts for generating results in Appendix A.

- **`MCE.sbatch`**: Slurm script for initiating relevant Python scripts on HPC.

#### Subfolder: `DAGs`
Contains scripts to test the robustness of cGNF to variations in architecture and hyper-parameter settings, replicating results from Appendix A.2.

Each folder from `Exp1` to `Exp5` contains the replication files for experiments 1 to 5.
- **`MCE.py`**: Generates and processes Monte Carlo samples, trains models, and computes estimates in parallel.
- **`loop.py`**: Initiates the execution of `MCE.py`.
- **`sum.py`**: Computes summary statistics.

#### Subfolders: `MCE_1`, `MCE_2`, `MCE_3`
Scripts for Monte Carlo experiments testing cGNF performance, replicating results from Appendix A.3.

- **`MCE_<1/2/3>.py`**: Generates and processes Monte Carlo samples, trains models, and computes estimates in parallel.
- **`init_MCE_<1/2/3>.py`**: Initiates the respective `MCE_<1/2/3>.py` script.
- **`sum_MCE_<1/2/3>.py`**: Computes summary statistics.
- **`plot_MCE_<1/2/3>.py`**: Plots summary statistics.
- **`est_<ATE/NDENIE/PSE>.py`**: Calculates the true values of average total effects, natural direct and indirect effects, and path-specific effects.

#### Subfolder: `CI_Coverage`
Scripts for testing the confidence interval coverage rate of cGNF, replicating results from Appendix A.4.

- **`MCE_bootstrap.py`**: Generates and processes bootstrap samples based on Monte Carlo samples, trains models, and computes estimates in parallel.
- **`bootstrap_for_MCE.py`**: Initiates `MCE_bootstrap.py`.
- **`MCE_for_bootstrap.py`**: Generates Monte Carlo samples.
- **`template_sbatch.sh`**: Slurm script for running `bootstrap_for_MCE.py` on HPC.
- **`submit_jobs.sh`**: Initiates `template_sbatch.sh` on HPC.
- **`sum_MCE_bootstrap.py`**: Computes 90% confidence intervals.
- **`plot_MCE_bootstrap.py`**: Plots 90% confidence intervals.

#### Subfolders: `Hyperparameter_1`, `Hyperparameter_2`
Scripts for testing the robustness of cGNF to variations in architecture and hyper-parameter settings, replicating results from Appendix A.5.

- **`Hyperparameters_<1/2>_<a, ..., e>.py`**: Produces Monte Carlo samples.
- **`init_hyperparameters_<1/2>.py`**: Initiates respective hyperparameter scripts.
- **`sum_hyperparameters_<1/2>.py`**: Computes summary statistics.
- **`plot_hyperparameters_<1/2>.py`**: Plots summary statistics.

#### Subfolder: `DML`
Scripts for testing the robustness of cGNF to variations in architecture and hyper-parameter settings, replicating results from Appendix A.6.

The folders `Compare_AIPW_10cat` and `Compare_AIPW_binary` replicate results comparing cGNF and AIPW-RF estimators.

In each folder:

- **`MCE.py`**: Generates and processes Monte Carlo samples, trains models, and computes estimates in parallel.
- **`loop.py`**: Initiates the execution of `MCE.py`.
- **`sum.py`**: Computes summary statistics.
- **`plot.py`**: Plots summary statistics.

The folder `cGNF_AIPW` contains scripts for estimating cGNF with AIPW:

- **`MCE_point.py`**: Generates and processes Monte Carlo samples, trains models, and computes estimates in parallel for each MCE dataset.
- **`loop_point.py`**: Initiates `MCE_point.py`.
- **`MCE_dml.py`**: Generates and processes Monte Carlo samples, trains models, and computes estimates in parallel to construct the AIPW-cGNF estimator.
- **`loop_dml.py`**: Initiates `MCE_dml.py`.
- **`sum.py`**: Computes the AIPW-cGNF estimator.
- **`template_sbatch.sh`**: Slurm script for running `MCE_dml.py` on HPC.
- **`submit_jobs.sh`**: Initiates `template_sbatch.sh` on HPC.

