import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

# Load the dataset
path = '/Users/jessezhou/Desktop/MCE_bootstrap/test_bin/'
data = pd.read_csv(path + 'final_90%CI.csv')

# Extracting data for plotting
mc_samples = data['Unnamed: 0']
ci_lower = data['5th percentile']
ci_upper = data['95th percentile']
ground_truth = 0.2

# Plotting
plt.figure(figsize=(12, 6))

# Create custom legend entries
custom_lines = [plt.Line2D([0], [0], color='black', marker='o', linestyle='None', markersize=3, label='Ground Truth (ATE = 0.2)'),
                plt.Line2D([0], [0], color='grey', lw=2, linestyle='-', label='CI Covering Ground Truth'),
                plt.Line2D([0], [0], color='grey', lw=2, linestyle='--', label='CI Not Covering Ground Truth')]

# Plot each CI and a smaller dot for the ground truth
for i in range(len(mc_samples)):
    # Determine if the CI covers the ground truth
    if ci_lower[i] <= ground_truth <= ci_upper[i]:
        linestyle = '-'  # Solid line for CIs that cover the ground truth
    else:
        linestyle = '--' # Dashed line for CIs that don't cover the ground truth

    plt.plot([mc_samples[i], mc_samples[i]], [ci_lower[i], ci_upper[i]], color='grey', linestyle=linestyle)
    plt.plot(mc_samples[i], ground_truth, 'o', color='black', markersize=3)

# Adding labels, title, and legend
plt.xlabel('Monte Carlo Sample Number')
plt.ylabel('Effect Size')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(handles=custom_lines)
plt.tight_layout()

plt.savefig(path + 'cGNF_Coverage_of_95%_CI_for_ATE.png', dpi=300)
plt.show()
