import os
import pandas as pd

# Define the path where the files are located
base_path = '/Users/jessezhou/Desktop/DISCRETE'
folder = '128k'
path = os.path.join(base_path, folder, '')

# List of file names to be appended
file_names = [f'128k_final_results_{i}.csv' for i in range(1, 11)]

# Initialize an empty DataFrame to store the combined results
final_results_df = pd.DataFrame()

# Iterate through the file names and read each CSV file
for file_name in file_names:
    file_path = os.path.join(path, file_name)
    temp_df = pd.read_csv(file_path)
    final_results_df = pd.concat([final_results_df, temp_df], ignore_index=True)

# Save the combined results to a new CSV file
final_results_file_path = os.path.join(path, '128k_final_results.csv')
final_results_df.to_csv(final_results_file_path, index=False)

final_results_df = pd.read_csv(final_results_file_path)


#cGNF

final_results_df['cGNF_ATE (A->Y)'] = final_results_df['E_Y_A_1_sim'] - final_results_df['E_Y_A_0_sim']
final_results_df['cGNF_PSE (A->Y)'] = final_results_df['E_Y_A_1_L_0_M_0_sim'] - final_results_df['E_Y_A_0_sim']
final_results_df['cGNF_PSE (A->L->Y)'] = final_results_df['E_Y_A_1_sim'] - final_results_df['E_Y_A_1_L_0_sim']
final_results_df['cGNF_PSE (A->M->Y)'] = final_results_df['E_Y_A_1_L_0_sim'] - final_results_df['E_Y_A_1_L_0_M_0_sim']
final_results_df['cGNF_ATE (A->M)'] = final_results_df['E_M_A_1_sim'] - final_results_df['E_M_A_0_sim']
final_results_df['cGNF_NDE'] = final_results_df['E_M_A_1_L_0_sim'] - final_results_df['E_M_A_0_sim']
final_results_df['cGNF_NIE'] = final_results_df['E_M_A_1_sim'] - final_results_df['E_M_A_1_L_0_sim']

# Save the DataFrame with new columns to a new CSV file or overwrite the previous file
final_results_df.to_csv(final_results_file_path, index=False)

# You can now use final_results_df for the subsequent analysis
results_df = final_results_df

# Define the true values
true_values = {
    'cGNF_ATE (A->Y)': 0.142693609,
    'cGNF_PSE (A->Y)': 0.109142679,
    'cGNF_PSE (A->L->Y)': 0.021937634,
    'cGNF_PSE (A->M->Y)': 0.011613296,
    'cGNF_ATE (A->M)': 0.112783829,
    'cGNF_NDE': 0.0923133,
    'cGNF_NIE': 0.020470529
}


# Compute the mean, variance, and MSE for the specified columns
columns_to_analyze = ['cGNF_ATE (A->Y)', 'cGNF_PSE (A->Y)', 'cGNF_PSE (A->L->Y)', 'cGNF_PSE (A->M->Y)', 'cGNF_ATE (A->M)',
                      'cGNF_NDE', 'cGNF_NIE']
summary_stats = {}

for col in columns_to_analyze:
    mean_value = results_df[col].mean()
    bias_value = mean_value - true_values[col]
    variance_value = results_df[col].var()
    mse_value = ((results_df[col] - true_values[col]) ** 2).mean()
    sd_value = variance_value ** (1/2)
    root_mse_value = mse_value ** (1/2)

    summary_stats[col] = {
        'Bias': bias_value,
        'SD': sd_value,
        'Root_MSE': root_mse_value,
    }


# Convert the summary statistics to a DataFrame and print/save if needed
summary_stats_df = pd.DataFrame.from_dict(summary_stats, orient='index')
print(summary_stats_df)

# Optionally, save the summary statistics to a CSV file
summary_stats_df.to_csv(path + '128k_summary_statistics.csv', index=True)

