import torch
import pickle
import pandas as pd
import os
import numpy as np
import random


def simDML(path="", dataset_name="", model_name="models", seed=None, covariate=None, treatment='', cat_list=[0, 1],
        outcome=None, inv_datafile_name='potential_outcome', num_draws=1):

    # Identify whether the system has a GPU, if yes it sets the device to "cuda:0" else "cpu"
    device = "cpu" if not (torch.cuda.is_available()) else "cuda:0"

    path_save = os.path.join(path, model_name)

    # Load the previously saved PyTorch model from the disk
    model = torch.load(path_save + '/_best_model.pt', map_location=device)

    # Load original dataset
    dataset_file_path = os.path.join(path, dataset_name + '.pkl')
    with open(dataset_file_path, 'rb') as f:
        data = pickle.load(f)

    # Extract the list of variables
    df = data['df']
    Z_Sigma = data['Z_Sigma']
    variable_list = df.columns.tolist()
    if treatment:
        loc_treatment = variable_list.index(treatment)

    # Move the model to the appropriate device (GPU if available or CPU)
    model = model.to(device)

    # Extract the adjacency matrix from the model's conditioner (after applying soft-thresholding) and move it to CPU. Convert it to numpy array.
    A_mat = model.getConditioners()[0].soft_thresholded_A().detach().cpu().numpy()

    # Fix: Corrected the method to calculate the number of samples
    n_mce_samples = len(df)

    # Define the dimensions of the adjacency matrix (number of nodes/variables)
    dim = A_mat.shape[0]

    # Set the model to evaluation mode
    model.eval()

    # Fix: Use the range function for iteration over num_draws
    results = []

    # Set the seed for random number generation. If not provided, select a random seed between 1 and 20000
    if seed is None:
        base_seed = random.randint(0, 2 ** 32 - 1)  # Full 32-bit integer range
    else:
        base_seed = seed

    for i in range(num_draws):

        # Derive a unique seed for each draw using base_seed and draw index
        seed = (base_seed + i) % (2**32)  # Ensure seed stays within 32-bit integer range

        # Setting the seed for random number generators in python, numpy and pytorch for reproducible results
        random.seed(seed)
        np.random.seed(seed=seed)
        torch.manual_seed(seed)

        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = True

        # Disable gradient calculation to save memory and computation during inference
        with torch.no_grad():
            # Import multivariate normal distribution from PyTorch distributions module
            from torch.distributions.multivariate_normal import MultivariateNormal

            # Define a multivariate normal distribution with mean 0 (torch.zeros) and identity covariance matrix (Z_Sigma)
            Z_do = MultivariateNormal(torch.zeros(dim), Z_Sigma)
            # Sample from the defined multivariate normal distribution
            z_do = Z_do.sample(torch.Size([n_mce_samples])).to(device)

            if treatment:
                # Create a tensor that contains all possible categories for our treatments
                all_a = torch.tensor(cat_list).unsqueeze(1).float()

                # Expand and clone the tensor for each treatment
                z_do_n = z_do.unsqueeze(1).expand(-1, all_a.shape[0], -1).clone().to(device)

                # Expand and clone the treatment tensor
                all_a_n = all_a.unsqueeze(0).expand(n_mce_samples, -1, -1).to(device)

                # Substitute treatment values
                z_do_n[:, :, [loc_treatment]] = all_a_n
            else:
                z_do_n = z_do.unsqueeze(1).expand(-1, 1, -1).clone().to(device)

            if covariate:
                n_covariate = len(covariate)
                boot_df = df.copy()

                loc_covariate = [variable_list.index(c) for c in covariate]

                for k in range(n_covariate):
                    all_c_values = boot_df.iloc[:, loc_covariate[k]].values
                    all_c_tensor = torch.tensor(all_c_values, dtype=torch.float).to(device)
                    all_c_tensor = all_c_tensor.unsqueeze(-1).unsqueeze(-1)
                    if treatment:
                        all_c_tensor = all_c_tensor.expand(-1, all_a.shape[0], -1).clone().to(device)
                    else:
                        all_c_tensor = all_c_tensor.expand(-1, 1, -1).clone().to(device)
                    z_do_n[:, :, [loc_covariate[k]]] = all_c_tensor

            # Reshape z_do_n for processing and move to appropriate device
            z_do_n = z_do_n.transpose(1, 0).reshape(-1, dim).to(device)

        # Counterfactual inference block
        with torch.no_grad():
            if covariate:
                if treatment:
                    indices = [loc_treatment] + loc_covariate
                    indices_tensor = torch.tensor(indices, dtype=torch.long)

                    cur_x_do_inv = model.invert(z_do_n, do_idx=[loc_treatment] + loc_covariate,
                                                do_val=torch.index_select(z_do_n, 1, indices_tensor))
                else:
                    indices = loc_covariate
                    indices_tensor = torch.tensor(indices, dtype=torch.long)

                    cur_x_do_inv = model.invert(z_do_n, do_idx=loc_covariate,
                                                do_val=torch.index_select(z_do_n, 1, indices_tensor))
            else:
                cur_x_do_inv = model.invert(z_do_n, do_idx=[loc_treatment],
                                            do_val=torch.narrow(z_do_n, 1, min([loc_treatment]),
                                                                len([loc_treatment])))

            cur_x_do_inv = cur_x_do_inv.view(-1, n_mce_samples, dim)

            # Reshape the tensor to 2D
            cur_x_do_inv_2d = cur_x_do_inv.reshape(-1, cur_x_do_inv.shape[-1])
            inv_output = pd.DataFrame(cur_x_do_inv_2d.cpu().detach().numpy())
            inv_output.columns = variable_list

            # Save to a CSV file
            # inv_output.to_csv(path + inv_datafile_name + f'.csv')

            # Fix: Extract only the outcome column
            outcome_column = inv_output[outcome]

            # Save and concatenate by column to results
            results.append(outcome_column)

    # Concatenate all the outcome columns generated from each draw into a DataFrame
    final_output = pd.concat(results, axis=1)
    final_output.columns = [f'{outcome}_draw_{i+1}' for i in range(num_draws)]

    # Save to a CSV file
    # output_file_path = os.path.join(path, inv_datafile_name + '.csv')
    # final_output.to_csv(output_file_path, index=False)

    return final_output
