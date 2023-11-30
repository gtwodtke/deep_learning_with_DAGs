import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from blau_bootstrap import run_simulation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: CPU_loop.py <node_id>")

    node_id = sys.argv[1]

    n_iterations = 40
    num_cores = min(40, os.cpu_count())  # Use at most 10 cores, but not more than available
    print(num_cores)
    results = Parallel(n_jobs=num_cores)(delayed(run_simulation)(i, node_id) for i in range(n_iterations))
    results_df = pd.DataFrame(results, columns=[f'E[Y(X={x})]' for x in range(97)] + [f'E[Y(U={x})]' for x in range(9)]
                                               + ['E[Y(X=9)]', 'E[Y(X=14)]', 'E[Y(X=9, U(X=14))]', 'E[Y(X=14, U(X=9))]',
                                                'E[Y(X=14)]', 'E[Y(X=18)]', 'E[Y(X=14, U(X=18))]', 'E[Y(X=18, U(X=14))]',
                                                'E[Y(X=18)]', 'E[Y(X=41)]', 'E[Y(X=18, U(X=41))]', 'E[Y(X=41, U(X=18))]',
                                                'E[Y(X=41)]', 'E[Y(X=61)]', 'E[Y(X=41, U(X=61))]', 'E[Y(X=61, U(X=41))]'] + ['Time_taken'])

    base_path = '/project/wodtke/cGNF_python_code/blau_duncan_1967'  # Adjust to your actual path
    folder = 'bootstrap'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'blau_bootstrap_final_results_{node_id}.csv')
    results_df.to_csv(output_file_path, index=False)
