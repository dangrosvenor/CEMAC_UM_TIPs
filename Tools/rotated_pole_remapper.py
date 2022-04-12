import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import iris
import iris.analysis.cartography
import iris.plot as iplt
import iris.quickplot as qplt
from iris.fileformats.um import structured_um_loading
import numpy as np

# file and variable to be remapped
fname = 'umnsaa_cb000'
variable = 'air_potential_temperature'
lvl = iris.Constraint(model_level_number=1)


# Load a UM file
with structured_um_loading():
    cube = iris.load_cube(fname, variable)

# extract and plot 2D field
theta = cube.extract(lvl)
qplt.contourf(theta, 15)
plt.gca().coastlines()
plt.show()
plt.cla()

# Get the rotated pole data
rot_pole = theta.coord('grid_latitude').coord_system.as_cartopy_crs()
# Get normal pole data
ll = ccrs.Geodetic()

# Create a rlat rlon map for rotated grid
rlats = theta.coords()[0]
rlons = theta.coords()[1]
X, Y = np.meshgrid(rlons.points, rlats.points)

# Create a map of standard lat lons
X_map = np.zeros_like(X)
Y_map = np.zeros_like(Y)
# For each point, this is not a nice rectangle
for i in range(0, len(rlons.points) ):
    for j in range(0, len(rlats.points) ):
        # the rotated coords
        rlon, rlat = [X[j, i], Y[j, i]]
        # transform rotated coord to regular lat lon
        target_xy = ll.transform_point(rlon, rlat, rot_pole)
        # Fill in are X Y meshgrids
        X_map[j, i] = target_xy[0]
        Y_map[j, i] = target_xy[1]

# Plot the remapped data
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.contourf(X_map,Y_map,theta.data, 60)
plt.show()
plt.cla()
