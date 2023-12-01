import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})  # Sets the global font size to 16

path = '/Users/jessezhou/Desktop/Midway_MCE_results/blau_duncan_1967/'

final_results = pd.read_csv(path +'final_standardized_ATE_UY_results.csv')

# Extract the X values (father's occupational status) from the 'Potential Outcomes' column
# Assuming the format is E[Y(X=x)] where x is the numeric value we need
final_results['X'] = final_results['Potential Outcomes'].str.extract(r'E\[Y\(U=(\d+)\)\]').astype(int)

# Plotting
plt.figure(figsize=(14, 8))

# Plot the point estimate with a solid line in grey scale
plt.plot(final_results['X'], final_results['point estimate'], label='Point Estimate', linestyle='-', color='black')

# Plot the 5th and 95th percentiles with the same dashed line style in grey scale and combined label
plt.plot(final_results['X'], final_results['5th percentile'], linestyle='--', color='grey')
plt.plot(final_results['X'], final_results['95th percentile'], label='90% Confidence Interval', linestyle='--', color='grey')

# Set the x-axis and y-axis labels
plt.xlabel("U: Son's education")
plt.ylabel("E[Y(U)]: Son's occupational status (SD Units)")

# Custom x-axis labels
education_labels = [
    "0: No schooling",
    "1: Elementary, 3-4 years",
    "2: Elementary, 5-7 years",
    "3: Elementary, 8 years",
    "4: High School, 1-3 years",
    "5: High School, 4 years",
    "6: College, 1-3 years",
    "7: College, 4 years",
    "8: College, 4+ years"
]

# Set the x-axis with custom labels
# The 'range(len(education_labels))' generates a list of positions for the labels from 0 to the length of the labels list
plt.xticks(range(len(education_labels)), education_labels, rotation=45, fontsize=12)

plt.xlim(0, 8)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend
plt.legend()
plt.tight_layout()
plt.savefig(path + "standardized_ATE_UY.png", dpi=300)
