import os
import sys
import pandas as pd
from joblib import Parallel, delayed
from zhou_bootstrap import run_simulation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: CPU_loop.py <node_id>")

    node_id = sys.argv[1]

    n_iterations = 40
    num_cores = min(40, os.cpu_count())  # Use at most 10 cores, but not more than available
    print(num_cores)
    results = Parallel(n_jobs=num_cores)(delayed(run_simulation)(i, node_id) for i in range(n_iterations))
    results_df = pd.DataFrame(results, columns=['E[Y(X=0.14 | C=0)]', 'E[Y(X=0.65 | C=0)]', 'E[Y(X=0.14 | C=1)]', 'E[Y(X=0.65 | C=1)]',
                                                'E[Y(X=0.14)]', 'E[Y(X=0.65)]', 'E[Y(X=0.14, C=1)]', 'E[Y(X=0.65, C=1)]',
                                                'E[Y(X=0.14)]', 'E[Y(X=0.65)]', 'E[Y(X=0.14, C=0)]', 'E[Y(X=0.65, C=0)]',
                                                'E[Y(X=0.14)]', 'E[Y(X=0.65)]', 'E[Y(X=0.14, L(X=0.65))]', 'E[Y(X=0.65, L(X=0.14))]',
                                                'E[Y(X=0.14, L(X=0.65), A(X=0.65))]', 'E[Y(X=0.65, L(X=0.14), A(X=0.14))]',
                                                'E[Y(X=0.14, L(X=0.65), A(X=0.65), C(X=0.65))]', 'E[Y(X=0.65, L(X=0.14), A(X=0.14), C(X=0.14))]',
                                                'Time_taken'])

    base_path = '/project/wodtke/cGNF_python_code/zhou_2019'  # Adjust to your actual path
    folder = 'bootstrap'  # Adjust to your actual folder
    path = os.path.join(base_path, folder)

    # Ensure the directory exists, if not, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Save the final results to a uniquely named CSV file
    output_file_path = os.path.join(path, f'zhou_bootstrap_final_results_{node_id}.csv')
    results_df.to_csv(output_file_path, index=False)
