import numpy as np

def simulate_generalized_lambda_distribution_4p(mu=0, sigma=1, lam=0, gamma=0, size=1):
    u = np.random.uniform(0, 1, size)
    return mu + (u**lam - (1 - u)**gamma) / sigma

# Number of Monte Carlo iterations
iterations = 100
obs = 10000000

# Initialize sums for the averages
sum_average_C = 0
sum_average_A = 0
sum_average_L = 0
sum_average_M = 0
sum_average_Y = 0

for _ in range(iterations):
    # Define probabilities for C
    prob_C = [0.3, 0.5, 0.2]  # Probabilities for C taking values 1, 2, and 3
    C = np.random.choice([1, 2, 3], size=obs, p=prob_C)

    # Treatment is set to zero for all observations
    A = np.full(obs, 1)


    # Define conditions for L
    def assign_L(C_val, A_val):
        if A_val == 1:
            if C_val == 1:
                return np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
            elif C_val == 2:
                return np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            else:  # C_val == 3
                return np.random.choice([1, 2, 3], p=[0.2, 0.3, 0.5])
        else:  # A_val == 0
            return np.random.choice([1, 2, 3], p=[0.6, 0.2, 0.2])


    # Assign L based on C and A
    L = np.array([assign_L(c, a) for c, a in zip(C, A)])

    # Mediator M, binary, with non-linear interaction
    # Logistic transformation to ensure binary outcome
    logit_M = -0.5 + 0.4 * A + 0.2 * C + 0.3 * L
    prob_M = 1 / (1 + np.exp(-logit_M))  # Sigmoid function for binary conversion
    M = np.random.binomial(1, prob_M, obs)

    # Outcome Y, binary, with interaction and non-linear terms
    # Logistic transformation to ensure binary outcome
    logit_Y = -0.5 + 0.3 * A + 0.1 * C + 0.3 * M + 0.3 * A * M + 0.3 * L
    prob_Y = 1 / (1 + np.exp(-logit_Y))  # Sigmoid function for binary conversion
    Y = np.random.binomial(1, prob_Y, obs)

    # Sum the averages for this iteration
    sum_average_C += np.mean(C)
    sum_average_A += np.mean(A)
    sum_average_L += np.mean(L)
    sum_average_M += np.mean(M)
    sum_average_Y += np.mean(Y)

# Calculate the overall averages
average_C = sum_average_C / iterations
average_A = sum_average_A / iterations
average_L = sum_average_L / iterations
average_M = sum_average_M / iterations
average_Y = sum_average_Y / iterations

print("Overall Average C:", average_C)
print("Overall Average A:", average_A)
print("Overall Average L:", average_L)
print("Overall Average M:", average_M)
print("Overall Average Y:", average_Y)
