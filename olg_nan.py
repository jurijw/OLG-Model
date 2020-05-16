# @http://web.econ.ku.dk/klemp/

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

grid = 200
xmin = 0
ymin = 0
xmax = 5
ymax = 7

a = 7
b = 0.33
p = -4.0
d = 0.6
h = 0
m = 8
rho = 0.4
n = 0.2

Dd = 1
De = 1
Df = 1
Dg = 1


def G(k_t, k_tplus1):
    # Note - when k_t is 0, W(k_t) is nan
    return S(W(k_t), R(k_tplus1)) / (1 + n) - k_tplus1

def S(W, R):
    if np.isnan(W):
        return 0
    
    utility = U(np.linspace(0, W, grid), W, R) # Calculate the utility function for a range of values # Potentially W / grid instead of W in the linspace function but doubt it
    
    # utility is sometimes evaluated as nan, meaning an error is thrown when trying max(utility)
    if np.isnan(utility):
        return 0

    # Find the max utility value along with its index
    max_utility = max(utility)
    max_utility_index = utility.index(max_utility)

    if np.isnan(max_utility):
        return 0
    else:
        return max_utility_index * W / grid


def W(k):
    try:
        return f(k) - k * (a * b * k ** (b - 1))
    except ZeroDivisionError:
        return float('nan')


def f(k):
    try:
        return a * k ** b
    except ZeroDivisionError:
        return float('nan')


def R(k):
    try:
        return a * b * k ** (b - 1) - d
    except ZeroDivisionError:
        return float('nan')  


def U(S, W, R):
    Utility_temp = v1(W - S) + v2((1 + R) * S) / (1 + rho)

    if np.isnan(Utility_temp):
        return float('nan')
    else:
        return Utility_temp


def v1(c):
    # Input is meant to be a list?
    for i in range(len(c)):
        if Dd + De * c[i] > 0: 
            return np.log(Dd + De * c[i])
        else:
            return float('nan')


def v2(c):
    for i in range(len(c)):
        if Df + Dg * c[i] > 0: 
            return np.log(Df + Dg * c[i])
        else:
            return float('nan')


# Setup grid
x, y = np.meshgrid(np.linspace(xmin, xmax, grid), np.linspace(ymin, ymax, grid))

z = np.zeros([grid, grid])

for i in range(grid): # FIX - might have to shift back one index because python arrays start at 0
    for j in range(grid):
        z[j][i] = G(xmin + i * (xmax - xmin) / grid, ymin + j * (ymax - ymin) / grid)

# Plot the thing
plt.contour(x, y, z)
plt.x_label = "k_t"
plt.show()

fig = plt.figure()
ax2 = plt.axes(projection="3d")
ax2.plot_surface(x, y, z)
plt.show()

# Plot individual funtions

# Line f and W
ax = plt.axes()
x_new = np.linspace(xmin, xmax, grid)
yf = f(np.linspace(xmin, xmax, grid)) / (1 + n)
wf = W(np.linspace(xmin, xmax, grid)) / (1 + n)
ax.plot(x_new, yf)
ax.plot(x_new, wf)
plt.show()