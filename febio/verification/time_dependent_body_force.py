import febio

# create a MeshDef object, mesh, reading in simpleblock.inp in abaqus format
mesh = febio.MeshDef('simpleblock.inp','abq')

# create a Model obect, model, that will be written to test.feb
# NOTE: all steps and modules for those steps are defined here
# default if blank is 1 step with module type "solid" 
model = febio.Model(modelfile='time_dependent_body_force.feb',steps=[{'BodyForce': 'solid'}])

#make a material
mat1 = febio.MatDef(matid=1,mname='Material 1',mtype='neo-Hookean',elsets=['exmymzm','exmypzm','exmymzp','exmypzp','expymzm','expypzm','expymzp','expypzp'],attributes={'density': '1.0', 'E': '1000.0','v': '0.3'})

#add the material to the model
model.addMaterial(mat1)

#make the geometry section of the model
model.addGeometry(mesh=mesh,mats=[mat1])

#add a loadcurve to the model
model.addLoadCurve(lc='1',lctype='smooth',points=[0,1,1,0])

#create a body force
loads = febio.Load(steps=1)
loads.addBodyForce(step=0,btype='const',attributes={'z': ['1','-9.81']})

#add the body force to the model
model.addLoad(load=loads)

#create a boundary condition to fix the bottom nodes
boundary = febio.Boundary(steps=1)
boundary.addFixed(nset=mesh.nsets['nzm'],dof='xyz')

#add the boundary condition to the model
model.addBoundary(boundary=boundary)

#create a control block for first step
ctrl = febio.Control()

#add the control block to the first step
model.addControl(ctrl=ctrl,step=0)

#generate the model file
model.writeModel()


