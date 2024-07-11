import numpy as np
# Function to interact with the environment (slot machines)
def play_slot_machine(action):
    probabilities = [0.1, 0.9, 0.5, 0.2]
    if np.random.uniform(0,1) <= probabilities[action]:
        return 100
    else:
        return 0