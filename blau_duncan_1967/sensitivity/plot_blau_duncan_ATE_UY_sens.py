import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})  # Sets the global font size to 16

path = '/Users/jessezhou/Desktop/Midway_MCE_results/blau_sens/'

# File paths for the datasets
files = [path + "standardized_ATE_UY_results_1.csv", path + "standardized_ATE_UY_results_2.csv",
         path + "standardized_ATE_UY_results_3.csv", path + "standardized_ATE_UY_results_4.csv"]

# Load the data from each file into separate dataframes
dataframes = [pd.read_csv(file) for file in files]

# Extracting the 'U' values and the corresponding 'E[Y(U)]' values from the datasets
u_values = [df['Potential Outcome'].str.extract(r'(\d+)').astype(int).squeeze() for df in dataframes]
y_values = [df['Value'] for df in dataframes]

# Line styles for differentiation
line_styles = ['solid', 'dashed', 'dotted', 'dashdot']

# Plotting the data
plt.figure(figsize=(14, 8))
for i in range(len(dataframes)):
    plt.plot(u_values[i], y_values[i], linestyle=line_styles[i], label=f'$\\rho_{{Z_U,Z_Y}} = {0.1 * i:.1f}$', color='black' )

# Setting the labels and title
plt.xlabel("U: Son's education")
plt.ylabel("E[Y(U)]: Son's occupational status (SD Units)")


# Custom x-axis labels
education_labels = [
    "0: No schooling",
    "1: Elementary, 3-4 years",
    "2: Elementary, 5-7 years",
    "3: Elementary, 8 years",
    "4: High School, 1-3 years",
    "5: High School, 4 years",
    "6: College, 1-3 years",
    "7: College, 4 years",
    "8: College, 4+ years"
]


plt.xticks(range(len(education_labels)), education_labels, rotation=45, fontsize=12)
plt.xlim(0, 8)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(path + "standardized_ATE_UY_sens.png", dpi=300)
