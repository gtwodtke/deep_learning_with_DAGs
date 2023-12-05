import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})  # Sets the global font size to 16

# Function to create a bar plot for a given column
def create_bar_plot(column, title, datasets, labels):
    # Number of datasets
    n_datasets = len(datasets)

    # Number of effects (assuming all datasets have the same number of effects)
    n_effects = len(datasets[0])

    # Set the positions of the bars on the x-axis
    bar_width = 0.15
    r = np.array(range(n_effects))
    positions = [r + bar_width * i for i in range(n_datasets)]

    # Calculate the middle position for each cluster
    middle_positions = r + bar_width * (n_datasets - 1) / 2

    # Create the bar plot
    plt.figure(figsize=(15, 8))
    for i, dataset in enumerate(datasets):
        plt.bar(positions[i], dataset[column], width=bar_width, color=str(0.2 * i), label=labels[i], zorder = 3)

    x_labels = [
        f"ATE$_{{A \\rightarrow Y}}$",
        f"PSE$_{{A \\rightarrow Y}}$",
        f"PSE$_{{A \\rightarrow L \\rightsquigarrow Y}}$",
        f"PSE$_{{A \\rightarrow M \\rightarrow Y}}$",
    ]

    plt.xticks(middle_positions, x_labels)
    plt.xlabel('Effects')
    plt.ylabel(title)

    # Create legend & Show graphic
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=0)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path + f"Hyperparameter_{title}.png", dpi=300)

path = '/Users/jessezhou/Desktop/Hyperparameters_1/'


# Load all datasets
file_paths = [path + '32k_1.csv', path + '32k_2.csv',
              path + '32k_3.csv', path + '32k_4.csv',
              path + '32k_5.csv']
datasets = [pd.read_csv(path) for path in file_paths]

# Labels for the datasets
dataset_labels = [
    "default hyperparameters",
    "default–one hidden layer from both nets",
    "default–1/4 of nodes from each layer",
    "batch size of 512, default otherwise",
    "learning rate of 0.001, default otherwise"
]

# Create the bar plots
create_bar_plot('Bias', 'Bias', datasets, dataset_labels)
create_bar_plot('SD', 'SD', datasets, dataset_labels)
create_bar_plot('Root_MSE', 'RMSE', datasets, dataset_labels)
