from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()
acceleration = options.getCmfdAcceleration()
relax_factor = options.getCmfdRelaxationFactor()
mesh_level = options.getCmfdMeshLevel()
num_azim=64
track_spacing=0.05
tolerance = 1E-5
log.set_log_level('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('XS_isot_assm_hdf5.h5')

uo2_id = materials['Fuel'].getId()
uo2Gd_id = materials['BA'].getId()
clad_1_id = materials['Tube1'].getId()
water_id = materials['Moderator'].getId()
clad_2_id = materials['Tube2'].getId()
clad_3_id = materials['Tube3'].getId()
clad_4_id = materials['Tube4'].getId()
clad_5_id = materials['Tube5'].getId()
###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circles = []
planes = []
planes.append(XPlane(x=-9.4854))
planes.append(XPlane(x=9.4854))
planes.append(YPlane(y=-9.4854))
planes.append(YPlane(y=9.4854))
circles.append(Circle(x=0.0, y=0.0, radius=0.572435))
circles.append(Circle(x=0.0, y=0.0, radius=0.613142))
circles.append(Circle(x=0.0, y=0.0, radius=0.412660))
circles.append(Circle(x=0.0, y=0.0, radius=0.474364))
for plane in planes: plane.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []
cells.append(CellBasic(universe=1, material=water_id, rings=3, sectors=8))
cells.append(CellBasic(universe=1, material=clad_1_id,sectors=8))
cells.append(CellBasic(universe=1, material=clad_2_id,sectors=8))
cells.append(CellBasic(universe=2, material=uo2_id,rings=3, sectors=8))
cells.append(CellBasic(universe=2, material=clad_3_id,sectors=8))
cells.append(CellBasic(universe=2, material=clad_4_id,sectors=8))
cells.append(CellBasic(universe=3, material=uo2Gd_id,rings=3, sectors=8))
cells.append(CellBasic(universe=3, material=clad_3_id,sectors=8))
cells.append(CellBasic(universe=3, material=clad_5_id,sectors=8))
#cells.append(CellBasic(universe=4, material=water_id,rings=3, sectors=8))
#cells.append(CellBasic(universe=4, material=clad_c_id,sectors=8))
#cells.append(CellBasic(universe=4, material=water_id,sectors=8))
cells.append(CellFill(universe=0, universe_fill=115))

cells[0].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[0])
cells[1].addSurface(halfspace=-1, surface=circles[1])
cells[2].addSurface(halfspace=+1, surface=circles[1])

cells[3].addSurface(halfspace=-1, surface=circles[2])
cells[4].addSurface(halfspace=+1, surface=circles[2])
cells[4].addSurface(halfspace=-1, surface=circles[3])
cells[5].addSurface(halfspace=+1, surface=circles[3])

cells[6].addSurface(halfspace=-1, surface=circles[2])
cells[7].addSurface(halfspace=+1, surface=circles[2])
cells[7].addSurface(halfspace=-1, surface=circles[3])
cells[8].addSurface(halfspace=+1, surface=circles[3])

#cells[9].addSurface(halfspace=-1, surface=circles[0])
#cells[10].addSurface(halfspace=+1, surface=circles[0])
#cells[10].addSurface(halfspace=-1, surface=circles[1])
#cells[11].addSurface(halfspace=+1, surface=circles[1])

cells[9].addSurface(halfspace=+1, surface=planes[0])
cells[9].addSurface(halfspace=-1, surface=planes[1])
cells[9].addSurface(halfspace=+1, surface=planes[2])
cells[9].addSurface(halfspace=-1, surface=planes[3])


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating 15 x 15 PWR lattice with Gd...')

lattice = Lattice(id=115, width_x=1.26472, width_y=1.26472)
lattice.setLatticeCells([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                         [2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2],
                         [2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2],
                         [2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2],
                         [2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])

###############################################################################
##########################     Creating Cmfd mesh    ##########################
###############################################################################
log.py_printf('NORMAL', 'Creating Cmfd mesh...')

mesh = Mesh(MOC, acceleration, relax_factor, mesh_level)

###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry(mesh)
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
geometry.addLattice(lattice)

geometry.initializeFlatSourceRegions()

###############################################################################
##########################   Creating Cmfd module    ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating cmfd module...')

cmfd = Cmfd(geometry)
cmfd.setOmega(1.0)

###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = ThreadPrivateSolver(geometry, track_generator, cmfd)
#solver = CPUSolver(geometry, track_generator)
solver.setNumThreads(num_threads)
solver.setSourceConvergenceThreshold(tolerance)
solver.convergeSource(max_iters)
solver.printTimerReport()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

#plotter.plot_tracks(track_generator)
#plotter.plot_segments(track_generator)
#plotter.plot_materials(geometry, gridsize=500)
#plotter.plot_cells(geometry, gridsize=500)
#plotter.plot_flat_source_regions(geometry, gridsize=500)
#plotter.plot_fluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')

