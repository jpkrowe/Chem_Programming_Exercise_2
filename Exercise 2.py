from numpy import *
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D


pathName = input("What is the pathname where the data is stored?")
molecule = input("What molecule is being analysed?")

r, theta = [], []
for x in arange(0.60, 1.90, 0.05):
    r.append(x)
for x in range(0, 180, 1):
    theta.append(x)

Energy = {}
count = 0
for i in r:
    for j in theta:
        fileLocation = pathName + "\\" + molecule + ".r" + '{:.2f}'.format(round(i, 2)) + "theta" + str(j) + ".0.out"
        if os.path.isfile(fileLocation):
            f = open(os.path.abspath(fileLocation), "r")
            for line in f:
                if "E(RHF)" in line:
                    l = line.split()
                    E = l[4]
                    Energy[(i, j)] = float(E)
            count += 1

# Count keeps track of how many files have been opened, if it is 0 no files have been found
if count == 0:
    print("No files have been found at that location for that molecule, please try again")
    exit()

# forms lists for x and y which are only the unique values of x and y
uniqueX = []
uniqueY = []
for coord, z in Energy.items():
    if coord[0] not in uniqueX:
        uniqueX.append(coord[0])
    if coord[1] not in uniqueY:
        uniqueY.append(coord[1])

X, Y = meshgrid(uniqueX, uniqueY)
Z = zeros((len(uniqueY), len(uniqueX)))

for i in range(len(uniqueX)):
    for j in range(len(uniqueY)):
        Z[j][i] = Energy[(uniqueX[i], uniqueY[j])]

fig = plt.figure()
ax = fig.gca(projection="3d")
surf = ax.plot_surface(X, Y, Z, cmap="jet")

ax.set_xlabel("r/Angstroms")
ax.set_ylabel("Theta/degrees")
ax.set_zlabel("Energy/Hartrees")

plt.savefig(str(molecule) + " potential surface")
