import numpy as np

def simulate_generalized_lambda_distribution_4p(mu=0, sigma=1, lam=0, gamma=0, size=1):
    u = np.random.uniform(0, 1, size)
    return mu + (u**lam - (1 - u)**gamma) / sigma

# Number of Monte Carlo iterations
iterations = 100
obs = 10000000

# Initialize sums for the averages
sum_average_C = 0
sum_average_A_x = 0
sum_average_L_x = 0
sum_average_M_x = 0
sum_average_A = 0
sum_average_Y = 0

for _ in range(iterations):
    # Confounder with Laplace distribution error
    C = np.random.laplace(0, 1, obs)

    # A_x is set to zero for all observations
    A_x = np.full(obs, 1)

    # Exposure-induced confounder with Tukey Lambda distribution error
    L_x = simulate_generalized_lambda_distribution_4p(mu=0, sigma=1, lam=0.3, gamma=0.7, size=obs) + 0.2*A_x + 0.2*C + 0.1*A_x*C

    # Mediator M_x with Cauchy distribution error
    M_x = np.random.standard_t(10, obs) + 0.1*A_x + 0.2*np.square(C) + 0.25*L_x + 0.15*A_x*L_x

    # A is set to one for all observations
    A = np.full(obs, 0)

    # Outcome with heteroscedastic error
    Y = np.random.normal(0, np.abs(C), obs) + 0.1*A + 0.1*np.square(C) + 0.2*M_x + 0.2*A*M_x + 0.25*np.square(L_x)

    # Sum the averages for this iteration
    sum_average_C += np.mean(C)
    sum_average_A_x += np.mean(A_x)
    sum_average_L_x += np.mean(L_x)
    sum_average_M_x += np.mean(M_x)
    sum_average_A += np.mean(A)
    sum_average_Y += np.mean(Y)

# Calculate the overall averages
average_C = sum_average_C / iterations
average_A_x = sum_average_A_x / iterations
average_L_x = sum_average_L_x / iterations
average_M_x = sum_average_M_x / iterations
average_A = sum_average_A / iterations
average_Y = sum_average_Y / iterations

print("Overall Average C:", average_C)
print("Overall Average A_x:", average_A_x)
print("Overall Average L_x:", average_L_x)
print("Overall Average M_x:", average_M_x)
print("Overall Average A:", average_A)
print("Overall Average Y:", average_Y)
