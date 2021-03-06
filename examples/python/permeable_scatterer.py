#!/usr/bin/env python

# This script uses BEM++ to solve a Helmholtz transmission problem. It
# calculates the field generated by a plane wave impinging on a
# permeable sphere from the -x direction.

# PART 1: Import the necessary modules #########################################

import sys
sys.path.append("..")

import numpy as np
from bempp import lib

# PART 2: Set quadrature and assembly options ##################################

# Create a quadrature strategy

accuracyOptions = lib.createAccuracyOptions()
accuracyOptions.doubleRegular.setRelativeQuadratureOrder(2)
accuracyOptions.singleRegular.setRelativeQuadratureOrder(2)
quadStrategy = lib.createNumericalQuadratureStrategy(
    "float64", "complex128", accuracyOptions)

# Set assembly options -- switch to ACA

options = lib.createAssemblyOptions()
options.switchToAca(lib.createAcaOptions())

# Combine the quadrature strategy and assembly options into an assembly context

context = lib.createContext(quadStrategy, options)

# PART 3: Define the system of integral equations to be solved #################

# Import mesh

grid = lib.createGridFactory().importGmshGrid(
    "triangular", "../../meshes/sphere-h-0.1.msh")

# Create a function space

pconsts = lib.createPiecewiseConstantScalarSpace(context, grid)

# Define material and wave parameters

rhoInt = 2.
rhoExt = 1.
kInt = 1.
kExt = 5.

# Create boundary operators

slpOpInt = lib.createHelmholtz3dSingleLayerBoundaryOperator(
    context, pconsts, pconsts, pconsts, kInt, "SLP_int")
slpOpExt = lib.createHelmholtz3dSingleLayerBoundaryOperator(
    context, pconsts, pconsts, pconsts, kExt, "SLP_ext")
dlpOpInt = lib.createHelmholtz3dDoubleLayerBoundaryOperator(
    context, pconsts, pconsts, pconsts, kInt, "DLP_int")
dlpOpExt = lib.createHelmholtz3dDoubleLayerBoundaryOperator(
    context, pconsts, pconsts, pconsts, kExt, "DLP_ext")
idOp = lib.createIdentityOperator(
    context, pconsts, pconsts, pconsts, "Id")

# Create blocks of the operator on the lhs of the equation...

lhsOp00 =  0.5 * idOp - dlpOpExt
lhsOp01 =  slpOpExt
lhsOp10 =  0.5 * idOp + dlpOpInt
lhsOp11 = -rhoInt / rhoExt * slpOpInt

# ... and combine them into a blocked operator

lhsOp = lib.createBlockedBoundaryOperator(
    context, [[lhsOp00, lhsOp01], [lhsOp10, lhsOp11]])

# Create a grid function representing the Dirichlet trace of the incident wave

def uIncData(point):
    x, y, z = point
    r = np.sqrt(x**2 + y**2 + z**2)
    return np.exp(1j * kExt * x)

uInc = lib.createGridFunction(context, pconsts, pconsts, uIncData)

# Create a grid function representing the Neumann trace of the incident wave

def uIncDerivData(point, normal):
    x, y, z = point
    nx, ny, nz = normal
    r = np.sqrt(x**2 + y**2 + z**2)
    return 1j * kExt * np.exp(1j * kExt * x) * nx

uIncDeriv = lib.createGridFunction(context, pconsts, pconsts, uIncDerivData,
                                   surfaceNormalDependent=True)

# Create elements of the right hand side of the equation

rhs = [uInc, None]

# PART 4: Discretize and solve the equations ###################################

# Create a GMRES solver

solver = lib.createDefaultIterativeSolver(lhsOp)
params = lib.defaultGmresParameterList(1e-8)
solver.initializeSolver(params)

# Solve the equation

solution = solver.solve(rhs)
print solution.solverMessage()

# PART 5: Extract the solution #################################################

# Extract the solution components (Dirichlet and Neumann traces of the
# total field)

uExt = solution.gridFunction(0)
uExtDeriv = solution.gridFunction(1)

# Combine them with the incident wave to yield the traces of the scattered field
# (uSc) and the field transmitted into the object (uInt)

uSc = uExt - uInc
uScDeriv = uExtDeriv - uIncDeriv

uInt = uExt
uIntDeriv = rhoInt / rhoExt * uExtDeriv

# PART 6: Evaluate the total field on part of the xy plane #####################

# Create the potential operators entering the Green's representation formula

slPotInt = lib.createHelmholtz3dSingleLayerPotentialOperator(context, kInt)
dlPotInt = lib.createHelmholtz3dDoubleLayerPotentialOperator(context, kInt)
slPotExt = lib.createHelmholtz3dSingleLayerPotentialOperator(context, kExt)
dlPotExt = lib.createHelmholtz3dDoubleLayerPotentialOperator(context, kExt)

# Create a grid of points

nPointsX = 201
nPointsY = 201
x, y, z = np.mgrid[-5:5:nPointsX*1j, -5:5:nPointsY*1j, 0:0:1j]
points = np.vstack((x.ravel(), y.ravel(), z.ravel()))

# Split the points into those located inside and outside the scatterer

inside = lib.areInside(grid, points)
outside = np.logical_not(inside)

# Use appropriate Green's representation formulas to evaluate the total field
# inside and outside the scatterer

evalOptions = lib.createEvaluationOptions()
valsExt = (- slPotExt.evaluateAtPoints(uScDeriv, points[:,outside], evalOptions)
           + dlPotExt.evaluateAtPoints(uSc, points[:,outside], evalOptions)
           + uIncData(points[:,outside]))
valsInt = (  slPotInt.evaluateAtPoints(uIntDeriv, points[:,inside], evalOptions)
           - dlPotInt.evaluateAtPoints(uInt, points[:,inside], evalOptions))

# Combine the results obtained for points inside and outside the scatterer
# in a single array

vals = np.empty(nPointsX * nPointsY, dtype=complex)
np.place(vals, outside, valsExt.ravel())
np.place(vals, inside, valsInt.ravel())

# Display the field plot

from bempp import visualization2 as vis
tvtkU = vis.tvtkStructuredGridData(
        points, vals, (nPointsX, nPointsY))
tvtkGrid = vis.tvtkGrid(grid)
vis.plotScalarData(tvtkGrid, None, tvtkU)

# Export the results into a VTK file

from tvtk.api import write_data
write_data(tvtkU, "u.vts")

# PART 6: Evaluate the far-field pattern of the scattered field ################

# Create the necessary potential operators

slFfPot = lib.createHelmholtz3dFarFieldSingleLayerPotentialOperator(context, kExt)
dlFfPot = lib.createHelmholtz3dFarFieldDoubleLayerPotentialOperator(context, kExt)

# Define a set of points on the unit sphere and evaluate the potentials

theta = np.linspace(0, 2*np.pi, 361)
points = np.vstack([np.cos(theta), np.sin(theta), 0. * theta])

farFieldPattern = (- slFfPot.evaluateAtPoints(uScDeriv, points, evalOptions)
                   + dlFfPot.evaluateAtPoints(uSc, points, evalOptions))
farFieldPattern = farFieldPattern.ravel()

# Display the graph

import pylab
pylab.polar(theta, abs(farFieldPattern))
pylab.title("Scattered field pattern")
pylab.show()
