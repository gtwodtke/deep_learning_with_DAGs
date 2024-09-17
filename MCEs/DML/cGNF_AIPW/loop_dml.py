import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from MCE_dml import run_simulation

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: bootstrap_for_MCE.py <node_id> <object>")

    node_id = sys.argv[1]
    n = sys.argv[2]

    n_iterations = 48
    num_cores = min(48, os.cpu_count())  # Use at most 48 cores, but not more than available
    print(f"Using {num_cores} cores for parallel processing.")

    # Parallel execution
    results = Parallel(n_jobs=num_cores)(
        delayed(run_simulation)(i, node_id, n) for i in range(n_iterations)
    )

    # Combine the results from each core into a single DataFrame
    combined_results_df = pd.concat(results, axis=1)

    # Define output path
    base_path = '/project/wodtke/cGNF_python_code/1k'
    folder = f'DF_{n}'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'Phat_final_results_{node_id}.csv')
    combined_results_df.to_csv(output_file_path, index=False)

