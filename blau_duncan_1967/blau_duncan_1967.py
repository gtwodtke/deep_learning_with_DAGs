import numpy as np
np.set_printoptions(precision=3, suppress=None)
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
import collections.abc
collections.Iterable = collections.abc.Iterable
import networkx as nx
from causalgraphicalmodels import CausalGraphicalModel
from cGNF import process, train, sim

base_path = '/project/wodtke/cGNF_python_code'  # Define the base path for file operations.
folder = 'blau_duncan_1967'  # Define the folder where files will be stored.
path = os.path.join(base_path, folder, '')  # Combines the base path and folder into a complete path.
dataset_name = 'blau_duncan_1967_cgnf'  # Define the name of the dataset.

if not (os.path.isdir(path)):  # checks if a directory with the name 'path' exists.
    os.makedirs(path)  # if not, creates a new directory with this name. This is where the logs and model weights will be saved.

# DAG SPECIFICATION
simDAG = CausalGraphicalModel(
    nodes = ["U", "V", "W", "X", "Y"],
    edges = [("V", "X"), ("V", "U"), ("X", "U"), ("X", "W"), ("X", "Y"), ("U", "W"), ("U", "Y"), ("W", "Y")])

print(simDAG.draw())  # Draws and prints the DAG.

# Converts the DAG to a pandas adjacency matrix.
df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)

print("------- Adjacency Matrix -------")
print(df_cDAG)  # Prints the adjacency matrix.

# Saves the adjacency matrix to a csv file.
df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=['U', 'V', 'W', 'X', 'Y'], seed=None)

train(path=path, dataset_name=dataset_name, path_save =path + 'point',
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60],
          int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

#ATE of X on Y
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=list(range(97)), moderator=None, mediator=None, outcome='Y', inv_datafile_name='ATE_XY')

#ATE of U on Y
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='U', cat_list=list(range(9)), moderator=None, mediator=None, outcome='Y', inv_datafile_name='ATE_UY')

#NDE & NIE of X on Y through U
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[9, 14], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='ND(I)E_XUY_1')

sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[14, 18], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='ND(I)E_XUY_2')

sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[18, 41], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='ND(I)E_XUY_3')

sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[41, 61], moderator=None, mediator=['U'], outcome='Y', inv_datafile_name='ND(I)E_XUY_4')

