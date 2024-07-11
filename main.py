import numpy as np
import matplotlib.pyplot as plt
import random

def bandit(action):
    if action == 0:
        p = 0.10
    elif action == 1:
        p = 0.20
    elif action == 2:
        p = 0.50
    else:
        p = 0.90
    if np.random.uniform(0, 1) <= p:
        return 100
    else:
        return 0