import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

base_path = '/Users/changhuizhou/Desktop/Midway_MCE_results/PSE'
folder = '128k_a'
path = os.path.join(base_path, folder, '')

# Reload the data from the provided CSV file
data = pd.read_csv(path + '128k_final_results.csv')

# Create the new columns as specified
data['cGNF_ATE (A->M)'] = data['E_M_A_1_sim'] - data['E_M_A_0_sim']
data['cGNF_NDE (A->M)'] = data['E_M_A_1_L_0_sim'] - data['E_M_A_0_sim']
data['cGNF_ATE (A->Y)'] = data['E_Y_A_1_sim'] - data['E_Y_A_0_sim']
data['cGNF_PSE (A->Y)'] = data['E_Y_A_1_L_0_M_0_sim'] - data['E_Y_A_0_sim']

# Revised code:

# Set up the figure with side-by-side subplots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

# Boxplot for cGNF_ATE (A->M)
axes[0].boxplot(data['cGNF_ATE (A->M)'])
axes[0].set_title('Boxplot of cGNF_ATE (A->M) at sample size of 128k with estop of 50')
axes[0].set_ylabel('Value')

# Boxplot for cGNF_NDE (A->M)
axes[1].boxplot(data['cGNF_NDE (A->M)'])
axes[1].set_title('Boxplot of cGNF_NDE (A->M) at sample size of 128k with estop of 50')
axes[1].set_ylabel('Value')

# Compute and display the summary statistics for cGNF_ATE (A->M)
desc_stats_ate = data['cGNF_ATE (A->M)'].describe()
stats_str_ate = '\n'.join([f'{key}: {value:.3f}' for key, value in desc_stats_ate.items()])
axes[0].text(1.25, data['cGNF_ATE (A->M)'].min(), stats_str_ate, ha='center', va='bottom')

# Compute and display the summary statistics for cGNF_NDE (A->M)
desc_stats_nde = data['cGNF_NDE (A->M)'].describe()
stats_str_nde = '\n'.join([f'{key}: {value:.3f}' for key, value in desc_stats_nde.items()])
axes[1].text(1.25, data['cGNF_NDE (A->M)'].min(), stats_str_nde, ha='center', va='bottom')

axes[0].yaxis.grid(True, which='both', linestyle='--', linewidth=0.5)
axes[1].yaxis.grid(True, which='both', linestyle='--', linewidth=0.5)

# Adjust layout
plt.tight_layout()

# Save the figure as an image with 300 DPI resolution
fig.savefig(path + 'effects_boxplots.png', dpi=300)

# Display the combined figure
plt.show()


