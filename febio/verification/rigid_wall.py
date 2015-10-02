import febio

# create a MeshDef object, mesh, reading in simpleblock.inp in abaqus format
mesh = febio.MeshDef('simpleblock.inp','abq')

# create a Model obect, model, that will be written to test.feb
# NOTE: all steps and modules for those steps are defined here
# default if blank is 1 step with module type "solid" 
model = febio.Model(modelfile='rigid_wall.feb',steps=[{'Displace': 'solid'}])

#make a material
mat1 = febio.MatDef(matid=1,mname='Material 1',mtype='neo-Hookean',elsets=['exmymzm','exmypzm','exmymzp','exmypzp','expymzm','expypzm','expymzp','expypzp'],attributes={'density': '1.0', 'E': '1000.0','v': '0.3'})

#add the material to the model
model.addMaterial(mat1)

#make the geometry section of the model
model.addGeometry(mesh=mesh,mats=[mat1])

#define a loadcurve
model.addLoadCurve(lc='1',lctype='linear',points=[0,0,1,.1])

#initialize a boundary condition object
boundary = febio.Boundary(steps=1)

#add a rigid_wall contact interface to boudary object
boundary.addContact(step=0,ctype='rigid_wall',master=['1','0','0','1','0'],slave=mesh.fsets['fzm'],attributes={'penalty': '1000.0'})

#add a fixed boundary condition to nodes of top z face
boundary.addFixed(nset=mesh.nsets['nzp'],dof='xyz')

#add the boudary conditions to the model
model.addBoundary(boundary)

#create a control block for step 1
ctrl = febio.Control()

#add the control block to the model
model.addControl(step=0,ctrl=ctrl)

#generate the model file
model.writeModel()


