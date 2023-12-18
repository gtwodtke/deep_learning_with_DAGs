import os
import pandas as pd

final_percentiles_df = pd.DataFrame()

for n in range(100):
    # Define the path where the files are located
    base_path = '/Users/jessezhou/Desktop/MCE_bootstrap/test_bin'
    folder = f'MCE_{n}'
    path = os.path.join(base_path, folder, '')

    # List of file names to be appended
    file_names = [f'MCE_bootstrap_final_results_{i}.csv' for i in range(1, 6)]

    # Initialize an empty DataFrame to store the combined results
    final_results_df = pd.DataFrame()

    # Iterate through the file names and read each CSV file
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        temp_df = pd.read_csv(file_path)
        final_results_df = pd.concat([final_results_df, temp_df], ignore_index=True)

    # Save the combined results to a new CSV file
    final_results_file_path = os.path.join(path, 'MCE_bootstrap_final_results.csv')
    final_results_df.to_csv(final_results_file_path, index=False)

    final_results_df = pd.read_csv(final_results_file_path)

    ##  EFFECT ESTIMATION
    final_results_df['ATE (A->Y)'] = final_results_df['E[Y(A=1)]'] - final_results_df['E[Y(A=0)]']

    final_results_df = final_results_df[[
        'ATE (A->Y)'
    ]]

    ## CONFIDENCE INTERVAL ESTIMATION
    percentiles = {}
    percentile_values = [5, 95]

    outcome_columns = [col for col in final_results_df]

    for column in outcome_columns:
        percentiles[column] = {}
        for p in percentile_values:
            percentiles[column][f'{p}th percentile'] = final_results_df[column].quantile(p / 100)

    # Convert the percentiles dictionary to a DataFrame
    percentiles_df = pd.DataFrame(percentiles).transpose()

    # Save the percentiles to a new CSV file
    percentiles_csv_path = os.path.join(path, f'MCE_boostrap_{n}_90%CI.csv')
    percentiles_df.to_csv(percentiles_csv_path)

    final_percentiles_df = pd.concat([final_percentiles_df, percentiles_df], ignore_index=True)

final_percentiles_df.to_csv(base_path + '/final_90%CI.csv')