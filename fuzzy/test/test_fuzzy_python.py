# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:54:21 2019

@author: rhann
"""

# Goal 1:

# Write a script in Python/Java (other other programming language of interest)
# that a) tries to find the issue we showed in that notebook above
# Add a bit to your script that runs this expression a few (~100) times,
# and prints the result each time
# Finally, add a piece that averages the results and prints the aggregate

# Goal 2:
# Get access to a system that has Docker installed
# (I will look for these for you, as well)
# Run your script in the Docker container and look at if the
# results are different from the "healthy" environment

import numpy as np
import sys

sys.setrecursionlimit(100000)

# function that will create flawed output by division. 
def first_function(N):
    step_one = 1/N
    step_two = sum([step_one for _ in range(N)])

    return step_two

# function that will create flawed output by taking any number, 
# take its square root, and immediately square it again. 
def second_function(N, B):
    for _ in range(B):
        M = N ** 0.5
        N = M ** 2

    return N

# function from paper by Parker et al(1997). 
# At around sequence number 30, the real answer is around 6
# It will, however, converge on 100. 
def u(K, dtype=float):
    K = dtype(K)
    if K == 0:
        return dtype(2)
    elif K == 1:
        return dtype(-4)
    else:
        uminus1 = u(K - 1)
        uminus2 = u(K - 2)
        return 111 - (1130/uminus1) + 3000/(uminus1 * uminus2)

# Same function, but with dtype. 
def u2(K, dtype=float):
    # premade outcomes which we know to be correct. 
    if K == 0:
        return dtype(2.0)
    elif K == 1:
        return dtype(-4.0)
    else:
        uminus2 = dtype(2.0)
        uminus1 = dtype(-4.0)
    for k in range(2, K+1):
        val = dtype(111) - (dtype(1130)/uminus1) + dtype(3000) / \
                   (uminus1 * uminus2)
        uminus2 = uminus1
        uminus1 = val
    return val


# X(30)
# X(30, dtype=np.float32)
# X(30, dtype=np.float64)
# The second function from the Parker paper. 
def X(N, dtype=float):
    N = dtype(N)
    # premade solution which we know to be correct. 
    if N == 0:
        return dtype(1.5100050721319)
    else:
        xminus1 = X(N - 1)
        return ((3*xminus1**4) - (20*xminus1**3) + (35*xminus1**2) - 24) / \
               ((4*xminus1**3) - (30*xminus1**2) + (70*xminus1 - 50))

# function that will run any other function a given number of times
# it will take the name of the function, a number of times to run, 
# and any number of input arguments for the function. 
def run_x_times(function, x, *args):
    result = []
    for _ in range(x):
        result += [function(*args)]
    #    sumresult = sum(result)/x, unused outcome
    #    gives result of running the function, along mean and std
    return result, np.mean(result), np.std(result)


# for every value of k up to 30:
# run u(k) ~ 100 times
# compute std and mean
# print k, mean, and std to screen
# will run the run_x_times function in a range of 0 to 30, 
# for two different kinds of (numpy) float. 
for t in [np.float32, np.float64]:
    for _ in range(30):
        # in the next line, replace u2 with the function to be run, 
        # and 100 with the number of times to run. 
        print(run_x_times(u2, 100, _, t))

# print(run_x_times(third_function, 100000, 100000))
# print(X(30))
# print(u(30))
