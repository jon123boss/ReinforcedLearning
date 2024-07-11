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
# Play the slot machines for the specified number of steps
for step in range(num_steps):
    # Determine whether to explore or exploit
    if np.random.rand() < epsilon:
        # Explore: choose a random action
        action = np.random.randint(num_actions)
    else:
        # Exploit: choose the action with the highest Q value
        action = np.argmax(Q)
    # Interact with the environment and get the reward
    reward = play_slot_machine(action)
    # Update the action count
    N[action] += 1
    # Update the Q value for the chosen action
    Q[action] += (reward - Q[action]) / N[action]
    # Print the final Q values
print("Q values for actions: 1:", round(Q[0]), "2:", round(Q[1]),"3:",round(Q[2]),"4:",round(Q[3]) )
