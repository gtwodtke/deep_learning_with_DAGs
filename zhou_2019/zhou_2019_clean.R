# sim

# Load the dataset
load("~/Desktop/programs/cGNF_python_code/zhou_2019/nlsy79_samples.RData")

# Make a copy of nlsy79_ed_b
nlsy79_ed_b_copy <- nlsy79_ed_b

# Now work on the copy
# Subset the data to keep only the required variables
nlsy79_ed_b_copy <- nlsy79_ed_b_copy[, c("dest", "origin", "college", "sex", "father", "hispanic", "black", "urban", "test_score", "educ_exp", "educ_mom", "num_sibs")]

# Convert 'TRUE' to 1 and 'FALSE' to 0 in 'college' column of the copy
nlsy79_ed_b_copy$college <- as.numeric(nlsy79_ed_b_copy$college)

# Rename the columns of the copy
colnames(nlsy79_ed_b_copy) <- c("Y", "X", "C", "S", "F", "H", "B", "U", "A", "L", "M", "N")

# Save the modified copy as a new RData file
save(nlsy79_ed_b_copy, file="~/Desktop/programs/cGNF_python_code/zhou_2019/zhou_2019_cgnf.RData")

# Convert and save the modified copy as a .csv file
write.csv(nlsy79_ed_b_copy, file="~/Desktop/programs/cGNF_python_code/zhou_2019/zhou_2019_cgnf.csv", row.names=FALSE)

# Calculate the 1st and 3rd quartiles for column O
quartiles_O <- quantile(nlsy79_ed_b_copy$X, probs = c(0.25, 0.75))

# Print the quartile values
print(quartiles_O)

