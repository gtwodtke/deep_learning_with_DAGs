import os
import pandas as pd

# Define the path where the files are located
base_path = '/Users/jessezhou/Desktop/Hyperparameter_2'
folder = '32k_5'
path = os.path.join(base_path, folder, '')

# List of file names to be appended
file_names = [f'32k_final_results_{i}.csv' for i in range(1, 11)]

# Initialize an empty DataFrame to store the combined results
final_results_df = pd.DataFrame()

# Iterate through the file names and read each CSV file
for file_name in file_names:
    file_path = os.path.join(path, file_name)
    temp_df = pd.read_csv(file_path)
    final_results_df = pd.concat([final_results_df, temp_df], ignore_index=True)

# Save the combined results to a new CSV file
final_results_file_path = os.path.join(path, '32k_final_results.csv')
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

#Linear Regression

final_results_df['reg_ATE (A->Y)'] = final_results_df['coef_YA'] + (final_results_df['coef_YL'] * final_results_df['coef_LA']) \
                                     + (final_results_df['coef_YM'] * final_results_df['coef_ML'] * final_results_df['coef_LA']) \
                                     + final_results_df['coef_YM'] * final_results_df['coef_MA']

final_results_df['reg_PSE (A->Y)'] = final_results_df['coef_YA']

final_results_df['reg_PSE (A->L->Y)'] = (final_results_df['coef_YL'] * final_results_df['coef_LA']) \
                                        + (final_results_df['coef_YM'] * final_results_df['coef_ML'] * final_results_df['coef_LA'])

final_results_df['reg_PSE (A->M->Y)'] = final_results_df['coef_YM'] * final_results_df['coef_MA']

final_results_df['reg_ATE (A->M)'] = final_results_df['coef_MA'] + (final_results_df['coef_ML'] * final_results_df['coef_LA'])
final_results_df['reg_NDE'] = final_results_df['coef_MA']
final_results_df['reg_NIE'] = final_results_df['coef_ML'] * final_results_df['coef_LA']

# Save the DataFrame with new columns to a new CSV file or overwrite the previous file
final_results_df.to_csv(final_results_file_path, index=False)

# You can now use final_results_df for the subsequent analysis
results_df = final_results_df

# Define the true values
true_values = {
    'cGNF_ATE (A->Y)': 0.324869557,
    'cGNF_PSE (A->Y)': 0.189000419,
    'cGNF_PSE (A->L->Y)': 0.085031005,
    'cGNF_PSE (A->M->Y)': 0.050838133,
    'cGNF_ATE (A->M)': 0.207101926,
    'cGNF_NDE': 0.127043695,
    'cGNF_NIE': 0.080058231,
    'reg_ATE (A->Y)': 0.324869557,
    'reg_PSE (A->Y)': 0.189000419,
    'reg_PSE (A->L->Y)': 0.085031005,
    'reg_PSE (A->M->Y)': 0.050838133,
    'reg_ATE (A->M)': 0.207101926,
    'reg_NDE': 0.127043695,
    'reg_NIE': 0.080058231
}


# Compute the mean, variance, and MSE for the specified columns
columns_to_analyze = ['cGNF_ATE (A->Y)', 'cGNF_PSE (A->Y)', 'cGNF_PSE (A->L->Y)', 'cGNF_PSE (A->M->Y)', 'cGNF_ATE (A->M)',
                      'cGNF_NDE', 'cGNF_NIE', 'reg_ATE (A->Y)', 'reg_PSE (A->Y)', 'reg_PSE (A->L->Y)', 'reg_PSE (A->M->Y)',
                      'reg_ATE (A->M)', 'reg_NDE', 'reg_NIE']
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
summary_stats_df.to_csv(path + '32k_summary_statistics.csv', index=True)

diff = {
    'Diff_ATE (A->Y)': abs(summary_stats_df.loc['cGNF_ATE (A->Y)']) - abs(summary_stats_df.loc['reg_ATE (A->Y)']),
    'Diff_PSE (A->Y)': abs(summary_stats_df.loc['cGNF_PSE (A->Y)']) - abs(summary_stats_df.loc['reg_PSE (A->Y)']),
    'Diff_PSE (A->L->Y)': abs(summary_stats_df.loc['cGNF_PSE (A->L->Y)']) - abs(summary_stats_df.loc['reg_PSE (A->L->Y)']),
    'Diff_PSE (A->M->Y)': abs(summary_stats_df.loc['cGNF_PSE (A->M->Y)']) - abs(summary_stats_df.loc['reg_PSE (A->M->Y)']),
    'Diff_ATE (A->M)': abs(summary_stats_df.loc['cGNF_ATE (A->M)']) - abs(summary_stats_df.loc['reg_ATE (A->M)']),
    'Diff_NDE': abs(summary_stats_df.loc['cGNF_NDE']) - abs(summary_stats_df.loc['reg_NDE']),
    'Diff_NIE': abs(summary_stats_df.loc['cGNF_NIE']) - abs(summary_stats_df.loc['reg_NIE'])
}

for diff_name, diff_values in diff.items():
    summary_stats_df.loc[diff_name] = diff_values



ratio = {
    'Ratio_ATE (A->Y)': summary_stats_df.loc['cGNF_ATE (A->Y)'] / summary_stats_df.loc['reg_ATE (A->Y)'],
    'Ratio_PSE (A->Y)': summary_stats_df.loc['cGNF_PSE (A->Y)'] / summary_stats_df.loc['reg_PSE (A->Y)'],
    'Ratio_PSE (A->L->Y)': summary_stats_df.loc['cGNF_PSE (A->L->Y)'] / summary_stats_df.loc['reg_PSE (A->L->Y)'],
    'Ratio_PSE (A->M->Y)': summary_stats_df.loc['cGNF_PSE (A->M->Y)'] / summary_stats_df.loc['reg_PSE (A->M->Y)'],
    'Ratio_ATE (A->M)': summary_stats_df.loc['cGNF_ATE (A->M)'] - summary_stats_df.loc['reg_ATE (A->M)'],
    'Ratio_NDE': summary_stats_df.loc['cGNF_NDE'] / summary_stats_df.loc['reg_NDE'],
    'Ratio_NIE': summary_stats_df.loc['cGNF_NIE'] / summary_stats_df.loc['reg_NIE']
}

for ratio_name, ratio_values in ratio.items():
    summary_stats_df.loc[ratio_name] = ratio_values



summary_stats_df.to_csv(path + '32k_summary_statistics.csv', index=True)
