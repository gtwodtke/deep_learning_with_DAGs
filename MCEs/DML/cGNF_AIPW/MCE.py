import numpy as np
import pandas as pd
import os
import time
from simulation_parallel_dml import sim

def run_simulation(i, node_id, n):
    print(f"Running simulation {i} on Process ID: {os.getpid()}")
    start_time = time.time()

    base_path = '/project/wodtke/cGNF_python_code/1k'
    folder = f'DF_{n}'  # Note the use of i to create a unique folder for each iteration
    path = os.path.join(base_path, folder)
    dataset_name = 'DF1_1k_loop'

    # ATE of X on Y
    test_results_df = sim(
        path=path,
        dataset_name=dataset_name,
        model_name='1k_loop',
        treatment='',
        confounder=['C1', 'C2'],
        cat_list=[0],
        outcome='A',
        inv_datafile_name=f'Phat_{node_id}_{i}',
        num_draws=5
    )

    # Return the DataFrame directly
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken for simulation {i}: {time_taken} seconds")

    return test_results_df
