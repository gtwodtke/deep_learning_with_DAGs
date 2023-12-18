import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from MCE_bootstrap import run_simulation

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: bootstrap_for_MCE.py <node_id> <object>")

    node_id = sys.argv[1]
    n = sys.argv[2]

    n_iterations = 40
    num_cores = min(40, os.cpu_count())  # Use at most 10 cores, but not more than available
    print(num_cores)
    results = Parallel(n_jobs=num_cores)(delayed(run_simulation)(i, node_id, n) for i in range(n_iterations))
    results_df = pd.DataFrame(results, columns=['E[Y(A=0)]', 'E[Y(A=1)]', 'Time_taken'])

    base_path = '/project/wodtke/cGNF_python_code/MCE_bootstrap'  # Adjust to your actual path
    folder = f'MCE_{n}'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'MCE_bootstrap_final_results_{node_id}.csv')
    results_df.to_csv(output_file_path, index=False)