import os
import pandas as pd

# Define the path where the files are located
base_path = '/Users/jessezhou/Desktop/Midway_MCE_results'
folder = 'zhou_2019'
path = os.path.join(base_path, folder, '')

# List of file names to be appended
file_names = [f'zhou_bootstrap_final_results_{i}.csv' for i in range(1, 16)]

# Initialize an empty DataFrame to store the combined results
final_results_df = pd.DataFrame()

# Iterate through the file names and read each CSV file
for file_name in file_names:
    file_path = os.path.join(path, file_name)
    temp_df = pd.read_csv(file_path)
    final_results_df = pd.concat([final_results_df, temp_df], ignore_index=True)


final_results_df['CATE(C=0)'] = final_results_df['E[Y(X=0.65 | C=0)]'] - final_results_df['E[Y(X=0.14 | C=0)]']
final_results_df['CATE(C=1)'] = final_results_df['E[Y(X=0.65 | C=1)]'] - final_results_df['E[Y(X=0.14 | C=1)]']
final_results_df['CDE(C=0)'] = final_results_df['E[Y(X=0.65, C=0)]'] - final_results_df['E[Y(X=0.14, C=0)]']
final_results_df['CDE(C=1)'] = final_results_df['E[Y(X=0.65, C=1)]'] - final_results_df['E[Y(X=0.14, C=1)]']
final_results_df['PSE(X-L-Y)'] = final_results_df['E[Y(X=0.65)]'] - final_results_df['E[Y(X=0.65, L(X=0.14))]']
final_results_df['PSE(X-A-Y)'] = final_results_df['E[Y(X=0.65, L(X=0.14))]'] - final_results_df['E[Y(X=0.65, L(X=0.14), A(X=0.14))]']
final_results_df['PSE(X-C-Y)'] = final_results_df['E[Y(X=0.65, L(X=0.14), A(X=0.14))]'] - final_results_df['E[Y(X=0.65, L(X=0.14), A(X=0.14), C(X=0.14))]']

final_results_df = final_results_df[[
    'CATE(C=0)', 'CATE(C=1)', 'CDE(C=0)', 'CDE(C=1)',
    'PSE(X-L-Y)', 'PSE(X-A-Y)', 'PSE(X-C-Y)'
]]

# Save the combined results to a new CSV file
final_results_file_path = os.path.join(path, 'zhou_bootstrap_final_results.csv')
final_results_df.to_csv(final_results_file_path, index=False)

# Calculate the 5th and 95th percentiles for each column
percentiles = {}
percentile_values = [5, 95]

outcome_columns = [col for col in final_results_df]

for column in outcome_columns:
    percentiles[column] = {}
    for p in percentile_values:
        percentiles[column][f'{p}th percentile'] = final_results_df[column].quantile(p/100)

# Convert the percentiles dictionary to a DataFrame
percentiles_df = pd.DataFrame(percentiles).transpose()

# Save the percentiles to a new CSV file
percentiles_csv_path = path + 'percentiles_zhou_2019_final_results.csv'
percentiles_df.to_csv(percentiles_csv_path)

