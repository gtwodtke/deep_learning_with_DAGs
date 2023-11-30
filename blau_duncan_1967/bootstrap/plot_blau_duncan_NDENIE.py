import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 16})  # Sets the global font size to 16

path = '/Users/changhuizhou/Desktop/Midway_MCE_results/blau_duncan_1967/'

results_df = pd.read_csv(path +'final_standardized_NDENIE_results.csv')

# Filter out NDE and NIE from the 'Effects' column
nde_results = results_df[results_df['Effects'].str.contains('NDE')]
nie_results = results_df[results_df['Effects'].str.contains('NIE')]

# Extract the unique group labels
labels = [
    "(x*=14, x=9)",
    "(x*=18, x=14)",
    "(x*=41, x=18)",
    "(x*=61, x=41)"
]

# The label locations and the width of the bars
x = range(len(labels))
width = 0.35

# Calculate the y values and the error bars for NDE and NIE
nde_y = nde_results['point estimate'].values
nde_yerr = [nde_results['point estimate'] - nde_results['5th percentile'],
            nde_results['95th percentile'] - nde_results['point estimate']]
nie_y = nie_results['point estimate'].values
nie_yerr = [nie_results['point estimate'] - nie_results['5th percentile'],
            nie_results['95th percentile'] - nie_results['point estimate']]

# Creating the plot with the requested changes
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')

# Plotting NDE bars with error bars
nde_error_bars = ax.bar([xi - width/2 for xi in x], nde_y, width, label='NDE(x*, x)', color='lightgrey', edgecolor='black', capsize=5, zorder = 2)
ax.errorbar([xi - width/2 for xi in x], nde_y, yerr=nde_yerr, fmt='none', ecolor='black', capsize=10, capthick=1)

# Plotting NIE bars with error bars
nie_error_bars = ax.bar([xi + width/2 for xi in x], nie_y, width, label='NIE(x*, x)', color='grey', edgecolor='black', capsize=5, zorder = 2)
ax.errorbar([xi + width/2 for xi in x], nie_y, yerr=nie_yerr, fmt='none', label='90% Confidence Interval', ecolor='black', capsize=10, capthick=1)

# Change y-axis label to 'Effect Estimate'
ax.set_ylabel('Effect Size (SD Units)')
ax.set_xlabel("(x*, x): Contrast between father's occupational status", labelpad=15)

# Modify x-axis labels to include parentheses and set custom x-axis tick labels
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=14)
ax.legend()

# Remove the top and right axes borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set the axes background color to white
ax.set_facecolor('white')

# Set grid
ax.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=0)
ax.grid(axis='x', color='white')

# Manually set the y-axis ticks to include -1 if necessary
current_ticks = ax.get_yticks()
if 0.3 not in current_ticks:
    ax.set_yticks(list(current_ticks) + [0.3])

plt.savefig(path + "standardized_NDENIE.png", dpi=300)



