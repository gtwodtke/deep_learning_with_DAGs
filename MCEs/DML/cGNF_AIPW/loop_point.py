import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from MCE_1k import run_simulation  # Ensure this module and function are properly defined and accessible

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: CPU_loop.py <node_id>")

    node_id = sys.argv[1]

    n_iterations = 40
    num_cores = min(40, os.cpu_count())  # Use at most 10 cores, but not more than available
    print(num_cores)
    results = Parallel(n_jobs=num_cores)(delayed(run_simulation)(i, node_id) for i in range(n_iterations))
    results_df = pd.DataFrame(results, columns=['E_Y_A_0_sim', 'E_Y_A_1_sim', 'E_Y_A_0_boot', 'E_Y_A_1_boot', 'ATEhat', 'Time_taken'])

    base_path = '/project/wodtke/cGNF_python_code'  # Adjust to your actual path
    folder = '1k'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'1k_final_results_{node_id}.csv')
    results_df.to_csv(output_file_path, index=False)

    combined_df = pd.concat([pd.read_csv(os.path.join(path, f'1k_final_results_{i}.csv')) for i in range(1, 6)],
                           ignore_index=True)
    combined_output_file_path = os.path.join(path, '1k_final_results.csv')
    combined_df.to_csv(combined_output_file_path, index=False)
