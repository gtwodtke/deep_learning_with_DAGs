import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})  # Sets the global font size to 16

path = '/Users/changhuizhou/Desktop/Midway_MCE_results/blau_duncan_1967/'

final_results = pd.read_csv(path +'final_standardized_ATE_XY_results.csv')

# Extract the X values (father's occupational status) from the 'Potential Outcomes' column
# Assuming the format is E[Y(X=x)] where x is the numeric value we need
final_results['X'] = final_results['Potential Outcomes'].str.extract(r'E\[Y\(X=(\d+)\)\]').astype(int)

# Plotting
plt.figure(figsize=(14, 8))

# Plot the point estimate with a solid line in grey scale
plt.plot(final_results['X'], final_results['point estimate'], label='Point Estimate', linestyle='-', color='black')

# Plot the 5th and 95th percentiles with the same dashed line style in grey scale and combined label
plt.plot(final_results['X'], final_results['5th percentile'], linestyle='--', color='grey')
plt.plot(final_results['X'], final_results['95th percentile'], label='90% Confidence Interval', linestyle='--', color='grey')

# Set the x-axis and y-axis labels
plt.xlabel("X: Father's occupational status")
plt.ylabel("E[Y(X)]: Son's occupational status (SD Units)")

# Set the x-axis limits to match the data and mark the ending point
plt.xticks(list(plt.xticks()[0]) + [96])
plt.xlim(0, 96)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend
plt.legend()
plt.savefig(path + "standardized_ATE_XY.png", dpi=300)
