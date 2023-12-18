import numpy as np
import pandas as pd
import os

for i in range(100):

    base_path = '/project/wodtke/cGNF_python_code/MCE_bootstrap'  # Define the base path for file operations.
    folder = f'MCE_{i}'  # Define the folder where files will be stored.
    path = os.path.join(base_path, folder, '')  # Combines the base path and folder into a complete path.
    dataset_name = '8k'  # Define the name of the dataset.

    if not (os.path.isdir(path)):  # Checks if a directory with the name 'path' exists.
        os.makedirs(
            path)  # If not, creates a new directory with this name. This is where the logs and model weights will be saved.

    ## DATA SIMULATION
    obs = 8000  # Sets the number of observations.

    C = np.random.binomial(n=1, p=0.5, size=obs)

    A = np.array([np.random.binomial(n=1, p=0.6) if c == 1 else np.random.binomial(n=1, p=0.4) for c in C])

    epsilon_Y = np.random.normal(0, 1, obs)
    Y = 0.2 * A + 0.4 * C + epsilon_Y

    df = pd.DataFrame({'C': C, 'A': A, 'Y': Y})

    df_filename = path + dataset_name + '.csv'
    df.to_csv(df_filename, index=False)

    ## DAG SPECIFICATION
    import collections.abc

    collections.Iterable = collections.abc.Iterable
    import networkx as nx
    from causalgraphicalmodels import CausalGraphicalModel

    simDAG = CausalGraphicalModel(
        nodes=["C", "A", "Y"],
        edges=[("C", "A"), ("C", "Y"),
               ("A", "Y")])

    df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)  # Converts the DAG to a pandas adjacency matrix.

    df_cDAG.to_csv(path + dataset_name + '_DAG.csv')