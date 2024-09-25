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
    # Confounder with Laplace distribution error
    C = np.random.laplace(0, 1, obs)

    # Treatment is set to zero for all observations
    A = np.full(obs, 1)

    # Exposure-induced confounder with Tukey Lambda distribution error
    L = simulate_generalized_lambda_distribution_4p(mu=0, sigma=1, lam=0.3, gamma=0.7, size=obs) + 0.2*A + 0.2*C + 0.1*A*C

    # Mediator with Cauchy distribution error
    M = np.random.standard_t(10, obs) + 0.1*A + 0.2*np.square(C) + 0.25*L + 0.15*A*L

    # Outcome with heteroscedastic error
    Y = np.random.normal(0, np.abs(C), obs) + 0.1*A + 0.1*np.square(C) + 0.2*M + 0.2*A*M + 0.25*np.square(L)

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
