import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from MCE_64k import run_simulation  # Ensure this module and function are properly defined and accessible

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: CPU_loop.py <node_id>")

    node_id = sys.argv[1]

    n_iterations = 48
    num_cores = min(48, os.cpu_count())  # Use at most 10 cores, but not more than available
    print(num_cores)
    results = Parallel(n_jobs=num_cores)(delayed(run_simulation)(i, node_id) for i in range(n_iterations))
    results_df = pd.DataFrame(results, columns=['ATEhat', 'Time_taken'])

    base_path = '/project/wodtke/cGNF_python_code/compare_10cat'  # Adjust to your actual path
    folder = '64k'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'64k_final_results_{node_id}.csv')
    results_df.to_csv(output_file_path, index=False)
