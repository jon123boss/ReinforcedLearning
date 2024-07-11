import numpy as np
# Function to interact with the environment (slot machines)
def play_slot_machine(action):
        # Define the payout probabilities for each slot machine
    probabilities = [0.1, 0.9, 0.5, 0.2]
            # Generate a random number to determine the reward
            if np.random.uniform(0,1) <= probabilities[action]:
                        return 100
            else:
                        return 0
            # Initialize Q and N lists with zeros
        num_actions = 4
Q = np.zeros(num_actions)
N = np.zeros(num_actions)
# Set the exploration rate (epsilon) and number of steps
epsilon = 0.4
num_steps = 1000