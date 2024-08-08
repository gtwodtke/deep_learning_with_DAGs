import numpy as np
import pandas as pd
import os
import networkx as nx
import time
from causalgraphicalmodels import CausalGraphicalModel
from processing_parallel import process
from training_parallel import train
from simulation_parallel_new import sim

def run_simulation(i, node_id):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()

    base_path = '/project/wodtke/cGNF_python_code/32k'
    folder = f'DF_{node_id}_{i}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder, '')
    dataset_name = 'DF1_32k_loop'

    ate_results_df = sim(path=path, dataset_name=dataset_name, model_name=path + '32k_loop', n_mce_samples=100000, treatment='A', cat_list=[0, 1],
       confounder = ["C1", "C2"], moderator=None, mediator=None, outcome='Y', inv_datafile_name='sim_boots_ate_32k')

    results_df = pd.concat([ate_results_df], ignore_index=True)

    values_list = results_df['Value'].tolist()

    end_time = time.time()
    time_taken = end_time - start_time

    values_list.append(time_taken)

    return values_list
