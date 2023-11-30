import os
import pandas as pd

# Define the path where the files are located
base_path = '/Users/changhuizhou/Desktop/Midway_MCE_results/blau_duncan_1967'
folder = 'ATE_UY'
path = os.path.join(base_path, folder, '')

# List of file names to be appended
file_names = [f'ATE_UY_final_results_{i}.csv' for i in range(1, 16)]

# Initialize an empty DataFrame to store the combined results
final_results_df = pd.DataFrame()

# Iterate through the file names and read each CSV file
for file_name in file_names:
    file_path = os.path.join(path, file_name)
    temp_df = pd.read_csv(file_path)
    final_results_df = pd.concat([final_results_df, temp_df], ignore_index=True)

# Save the combined results to a new CSV file
final_results_file_path = os.path.join(path, 'ATE_UY_final_results.csv')
final_results_df.to_csv(final_results_file_path, index=False)

# Calculate the 5th and 95th percentiles for each potential outcome column
percentiles = {}
percentile_values = [5, 95]

# We don't need to include "Time_taken" in the percentile calculations
outcome_columns = [col for col in final_results_df if col.startswith('E[Y(U=')]

for column in outcome_columns:
    percentiles[column] = {}
    for p in percentile_values:
        percentiles[column][f'{p}th percentile'] = final_results_df[column].quantile(p/100)

# Convert the percentiles dictionary to a DataFrame
percentiles_df = pd.DataFrame(percentiles).transpose()

# Save the percentiles to a new CSV file
percentiles_csv_path = path + 'percentiles_ATE_UY_final_results.csv'
percentiles_df.to_csv(percentiles_csv_path)

percentiles_df = pd.read_csv(path + '/percentiles_ATE_UY_final_results.csv')
percentiles_df = percentiles_df.rename(columns={'Unnamed: 0': 'Potential Outcomes'})
percentiles_df = percentiles_df.set_index('Potential Outcomes')

point_results = pd.read_csv(base_path + '/point_ATE_UY_results.csv')

# Set the 'Effects' column as the index and rename the 'Values' column
point_results.set_index('Effects', inplace=True)
point_results.rename(columns={'Values': 'point estimate'}, inplace=True)

# Merge the point estimates with the percentiles DataFrame
final_results = percentiles_df.join(point_results)

# Save the merged DataFrame to a new CSV file
final_results.to_csv(base_path + '/final_ATE_UY_results.csv')
