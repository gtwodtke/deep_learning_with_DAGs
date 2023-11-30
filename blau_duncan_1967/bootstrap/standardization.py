import pandas as pd


first_path = '/Users/changhuizhou/Desktop/programs/cGNF_python_code/blau_duncan_1967/'

# Load the first dataset
data_first = pd.read_csv(first_path + 'blau_duncan_1967_cgnf.csv')

# Calculate the mean and standard deviation for column 'Y'
mean_Y = data_first['Y'].mean()
std_dev_Y = data_first['Y'].std()

# Load the second dataset
second_path = '/Users/changhuizhou/Desktop/Midway_MCE_results/blau_duncan_1967/'
data_second = pd.read_csv(second_path + 'final_NDENIE_results.csv')

# Standardize all values except for the first column using the calculated mean and std_dev
data_second_standardized = data_second.copy()  # Make a copy to avoid changing original data

# We assume that the first column should not be standardized as per the user's instructions
for column in data_second_standardized.columns[1:]:
    data_second_standardized[column] = data_second_standardized[column] / std_dev_Y

data_second_standardized.to_csv(second_path + '/final_standardized_NDENIE_results.csv')
