import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Times New Roman"

# Reading datasets
path = '/Users/jessezhou/Desktop/DISCRETE/'

data_2k = pd.read_csv(path + "2k/2k_summary_statistics.csv", index_col=0)
data_4k = pd.read_csv(path + "4k/4k_summary_statistics.csv", index_col=0)
data_8k = pd.read_csv(path + "8k/8k_summary_statistics.csv", index_col=0)
data_16k = pd.read_csv(path + "16k/16k_summary_statistics.csv", index_col=0)
data_32k = pd.read_csv(path + "32k/32k_summary_statistics.csv", index_col=0)
data_64k = pd.read_csv(path + "64k/64k_summary_statistics.csv", index_col=0)
data_128k = pd.read_csv(path + "128k/128k_summary_statistics.csv", index_col=0)

# Specify the effects of interest
desired_effects = [
    "cGNF_ATE (A->Y)",
    "cGNF_PSE (A->Y)",
    "cGNF_PSE (A->L->Y)",
    "cGNF_PSE (A->M->Y)",
    "cGNF_ATE (A->M)",
    "cGNF_NDE",
    "cGNF_NIE"
]

# Extract the data for the desired effects
sample_sizes = [2000, 4000, 8000, 16000, 32000, 64000, 128000]

bias_values_cgnf = {
    effect: [
        data_2k.loc[effect, 'Bias'],
        data_4k.loc[effect, 'Bias'],
        data_8k.loc[effect, 'Bias'],
        data_16k.loc[effect, 'Bias'],
        data_32k.loc[effect, 'Bias'],
        data_64k.loc[effect, 'Bias'],
        data_128k.loc[effect, 'Bias']
    ] for effect in desired_effects
}

sd_values_cgnf = {
    effect: [
        data_2k.loc[effect, 'SD'],
        data_4k.loc[effect, 'SD'],
        data_8k.loc[effect, 'SD'],
        data_16k.loc[effect, 'SD'],
        data_32k.loc[effect, 'SD'],
        data_64k.loc[effect, 'SD'],
        data_128k.loc[effect, 'SD']
    ] for effect in desired_effects
}

rootmse_values_cgnf = {
    effect: [
        data_2k.loc[effect, 'Root_MSE'],
        data_4k.loc[effect, 'Root_MSE'],
        data_8k.loc[effect, 'Root_MSE'],
        data_16k.loc[effect, 'Root_MSE'],
        data_32k.loc[effect, 'Root_MSE'],
        data_64k.loc[effect, 'Root_MSE'],
        data_128k.loc[effect, 'Root_MSE']
    ] for effect in desired_effects
}

label_effect = [f"ATE$_{{A \\rightarrow Y}}$",
                f"PSE$_{{A \\rightarrow Y}}$",
                f"PSE$_{{A \\rightarrow L \\rightsquigarrow Y}}$",
                f"PSE$_{{A \\rightarrow M \\rightarrow Y}}$",
                f"ATE$_{{A \\rightarrow M}}$",
                f"NDE$_{{A \\rightarrow M}}$",
                f"NIE$_{{A \\rightarrow L \\rightarrow M}}$"]

# Adjusting the styles to make them unique for each effect

# Define unique styles for the lines
line_styles_unique = ['-', '--', '-.', ':', (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1)), (0, (5, 10))]
marker_unique = ['o', 's', '^', '+', 'x', 'd', 'p']  # circle, square, triangle_up, triangle_down, triangle_left, triangle_right, pentagon
colors_unique = ['black', 'grey', 'black', 'grey', 'black', 'grey', 'black']

# Plotting Bias with unique styles
plt.figure(figsize=(10, 7))
for idx, effect in enumerate(desired_effects):
    plt.plot(sample_sizes, bias_values_cgnf[effect], label=label_effect[idx], linestyle=line_styles_unique[idx], color=colors_unique[idx], marker=marker_unique[idx])
# plt.title("Bias for Specified cGNF Effects")
plt.xlabel("Sample Size")
plt.ylabel("Bias")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(path + "Bias_for_Specified_cGNF_Effects.png", dpi=300)
plt.show()

# Plotting SD with unique styles
plt.figure(figsize=(10, 7))
for idx, effect in enumerate(desired_effects):
    plt.plot(sample_sizes, sd_values_cgnf[effect], label=label_effect[idx], linestyle=line_styles_unique[idx], color=colors_unique[idx], marker=marker_unique[idx], markersize=6)
# plt.title("Standard Deviation for Specified cGNF Effects")
plt.xlabel("Sample Size")
plt.ylabel("Standard Deviation")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.ylim(bottom=0)  # Set the lower limit of y-axis to 0
plt.tight_layout()
plt.savefig(path + "SD_for_Specified_cGNF_Effects.png", dpi=300)
plt.show()

# Plotting Root_MSE with unique styles
plt.figure(figsize=(10, 7))
for idx, effect in enumerate(desired_effects):
    plt.plot(sample_sizes, rootmse_values_cgnf[effect], label=label_effect[idx], linestyle=line_styles_unique[idx], color=colors_unique[idx], marker=marker_unique[idx])
# plt.title("Root_MSE for Specified cGNF Effects")
plt.xlabel("Sample Size")
plt.ylabel("RMSE")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.ylim(bottom=0)  # Set the lower limit of y-axis to 0
plt.tight_layout()
plt.savefig(path + "Root_MSE_for_Specified_cGNF_Effects.png", dpi=300)
plt.show()


bias_values_cgnf_tab = pd.DataFrame(bias_values_cgnf, index=['2k', '4k', '8k', '16k', '32k', '64k', '128k']).T.round(3)
sd_values_cgnf_tab = pd.DataFrame(sd_values_cgnf, index=['2k', '4k', '8k', '16k', '32k', '64k', '128k']).T.round(3)
rootmse_values_cgnf_tab = pd.DataFrame(rootmse_values_cgnf, index=['2k', '4k', '8k', '16k', '32k', '64k', '128k']).T.round(3)


# Combining all four tables: Bias, SD, Root_MSE, and Ratio Root_MSE
combined_df = pd.concat([
    bias_values_cgnf_tab.add_prefix("Bias_"),
    sd_values_cgnf_tab.add_prefix("SD_"),
    rootmse_values_cgnf_tab.add_prefix("RootMSE_"),
], axis=1)

# Saving the combined table to an Excel file
combined_df.to_excel(path + "combined_data.xlsx")
