import numpy as np
np.set_printoptions(precision=3, suppress=None)
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
import collections.abc
collections.Iterable = collections.abc.Iterable
import networkx as nx
from causalgraphicalmodels import CausalGraphicalModel
from cGNF import process, train, sim


base_path = '/Users/jessezhou/Desktop/programs/cGNF_python_code'  # Define the base path for file operations.
folder = 'zhou_2019'  # Define the folder where files will be stored.
path = os.path.join(base_path, folder, '')  # Combines the base path and folder into a complete path.
dataset_name = 'zhou_2019_cgnf'  # Define the name of the dataset.

if not (os.path.isdir(path)):  # checks if a directory with the name 'path' exists.
    os.makedirs(path)  # if not, creates a new directory with this name. This is where the logs and model weights will be saved.


# DAG SPECIFICATION
simDAG = CausalGraphicalModel(
    nodes = ["Y", "X", "C", "S", "F", "H", "B", "U", "A", "L", "M", "N"],
    edges = [("X", "Y"), 
             ("X", "C"), 
             ("C", "Y"),  
             ("X", "A"), ("X", "L"), 
             ("A", "C"), ("A", "Y"),
             ("L", "C"), ("L", "Y"),
             ("L", "A"),  #L1 -> L2
             ("S", "X"), ("F", "X"), ("H", "X"), ("B", "X"), ("U", "X"),  ("M", "X"), ("N", "X"), 
             ("S", "A"), ("S", "L"), ("S", "C"), ("S", "Y"), 
             ("F", "A"), ("F", "L"), ("F", "C"), ("F", "Y"),
             ("H", "A"), ("H", "L"), ("H", "C"), ("H", "Y"),
             ("B", "A"), ("B", "L"), ("B", "C"), ("B", "Y"),
             ("U", "A"), ("U", "L"), ("U", "C"), ("U", "Y"),
             ("M", "A"), ("M", "L"), ("M", "C"), ("M", "Y"),
             ("N", "A"), ("N", "L"), ("N", "C"), ("N", "Y"), ])

print(simDAG.draw())  # Draws and prints the DAG.

# Converts the DAG to a pandas adjacency matrix.
df_cDAG = nx.to_pandas_adjacency(simDAG.dag, dtype=int)

print("------- Adjacency Matrix -------")
print(df_cDAG)  # Prints the adjacency matrix.

# Saves the adjacency matrix to a csv file.
df_cDAG.to_csv(path + dataset_name + '_DAG.csv')

process(path=path, dataset_name=dataset_name, dag_name=dataset_name + '_DAG', test_size=0.2, cat_var=['C', 'S', 'F', 'H', 'B', 'U', 'L', 'M', 'N'], seed=None)

train(path=path, dataset_name=dataset_name, path_save =path + 'point',  # General parameters
          trn_batch_size=128, val_batch_size=4096, learning_rate=1e-4, seed=None, nb_epoch=50000,
          emb_net=[100, 90, 80, 70, 60],
          int_net=[60, 50, 40, 30, 20], nb_estop=50, val_freq=1)

#Conditional mobility
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[0.14, 0.65], moderator='C', mediator=None, outcome='Y', inv_datafile_name='conditional')

#Controlled mobility
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[0.14, 0.65], moderator=None, mediator=['C=1'], outcome='Y', inv_datafile_name='controlled_1')

sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[0.14, 0.65], moderator=None, mediator=['C=0'], outcome='Y', inv_datafile_name='controlled_0')

#Path-specific effects
sim(path=path, dataset_name=dataset_name, path_save =path + 'point', n_mce_samples = 10000, treatment='X', cat_list=[0.14, 0.65], moderator=None, mediator=['L', 'A', 'C'], outcome='Y', inv_datafile_name='PSE')
