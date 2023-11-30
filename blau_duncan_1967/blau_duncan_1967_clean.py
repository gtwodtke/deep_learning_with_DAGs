import pandas as pd
import os

base_path = '/Users/changhuizhou/Desktop/programs/cGNF_python_code'  # Define the base path for file operations.
folder = 'blau_duncan_1967'  # Define the folder where files will be stored.
path = os.path.join(base_path, folder, '')  # Combines the base path and folder into a complete path.
dataset_name = 'blau_duncan_1967_cgnf'  # Define the name of the dataset.


# Creating an empty Dataframe with column names only
df_ds1 = pd.DataFrame(columns=['U', 'V', 'W', 'X', 'Y'])

rows_list = []

# Dataset and Codebook link https://www.icpsr.umich.edu/web/ICPSR/studies/6162 , https://www.icpsr.umich.edu/web/ICPSR/studies/6162/datadocumentation
with open(path + f'DS1_1962_ssv.txt', "r") as f:
    lines = f.readlines()

    count = 0  # line counter
    # extract the lines and the respective data/variables from the location specified in the dataset codebook.
    for line in lines:
        count += 1
        #     print(line[-1])
        #     print("Line{} [{}]: {}".format(count, len(line), line.strip()))

        R = float(line[30 - 1:30 - 1 + 1])  # Race
        U = float(line[166 - 1:166 - 1 + 2])  # Son's Educational Attainment
        V = float(line[168 - 1:168 - 1 + 2])  # Father's Educational Attainment
        W = float(line[131 - 1:131 - 1 + 3])  # Son's SocioEconomicStatus 1st Job
        X = float(line[143 - 1:143 - 1 + 3])  # Father's SocioEconomicStatus
        Y = float(line[119 - 1:119 - 1 + 3])  # Son's SocioEconomicStatus 1962

        # Filer only white male as per Duncan's setup
        if R == 0:
            rows_list.append({'U': U, 'V': V, 'W': W, 'X': X, 'Y': Y})

# Convert the list of dictionaries to a DataFrame
new_rows_df = pd.DataFrame(rows_list)

# Concatenate the new DataFrame with the original df_ds1
df_ds1 = pd.concat([df_ds1, new_rows_df], ignore_index=True)

exclude_nans_V = [9.0]
mask = df_ds1['V'].isin(exclude_nans_V)
df_ds1 = df_ds1[~mask]
exclude_nans_WXY = [99.0]
mask = df_ds1['W'].isin(exclude_nans_WXY)
df_ds1 = df_ds1[~mask]
mask = df_ds1['X'].isin(exclude_nans_WXY)
df_ds1 = df_ds1[~mask]
mask = df_ds1['Y'].isin(exclude_nans_WXY)
df_ds1 = df_ds1[~mask]

# Saving the pre-processed dataset to uncompressed csv file
df_ds1.to_csv(path + dataset_name + f'.csv', index=False)

# Calculate the percentiles for  X
percentiles = [10, 25, 50, 75, 90]
percentile_values = df_ds1['X'].quantile([p / 100 for p in percentiles]).to_dict()

# Show the percentile values
print(percentile_values)

