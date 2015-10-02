import febio

# create a MeshDef object, mesh, reading in simpleblock.inp in abaqus format
mesh = febio.MeshDef('simpleblock.inp','abq')

# create a Model obect, model, that will be written to test.feb
# NOTE: all steps and modules for those steps are defined here
# default if blank is 1 step with module type "solid" 
model = febio.Model(modelfile='multi_step.feb',steps=[{'Displace': 'solid'}, {'Load': 'solid'}])

#make a material
mat1 = febio.MatDef(matid=1,mname='Material 1',mtype='neo-Hookean',
elsets=['exmymzm','exmypzm','exmymzp','exmypzp','expymzm','expypzm','expymzp','expypzp'],attributes={'density': '1.0', 'E': '1000.0','v': '0.3'})

#add the material to the model
model.addMaterial(mat1)

#make the geometry section of the model
model.addGeometry(mesh=mesh,mats=[mat1])

#define a loadcurve
model.addLoadCurve(lc='1',lctype='linear',points=[0,0,1,1])
model.addLoadCurve(lc='2',lctype='linear',points=[1,0,2,1])

#initialize a boundary condition object
boundary = febio.Boundary(steps=2)
#add a fixed boundary condition to bottom z nodes
boundary.addFixed(nset=mesh.nsets['nzm'],dof='xyz')
#add a prescribed displace to top z nodes for step 1
boundary.addPrescribed(step=0,nset=mesh.nsets['nzp'],dof='z',lc='1',scale='0.1')
#add a relative prescribed displacement to top z nodes for step 2
boundary.addPrescribed(step=1,nset=mesh.nsets['nzp'],dof='z',lc='2',scale='0.2',ptype='relative')

#add boundary conditions to model
model.addBoundary(boundary=boundary)

#create a control block
ctrl = febio.Control()

#add the control block to the model step 1
model.addControl(step=0,ctrl=ctrl)
#add same control block to step 2
model.addControl(step=1,ctrl=ctrl)

#generate the model file
model.writeModel()
