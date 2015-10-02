import febio
# create a MeshDef object, mesh, reading in simpleblock.inp in abaqus format
mesh = febio.MeshDef('simpleblock.inp','abq')

# create a Model obect, model, that will be written to test.feb
# NOTE: all steps and modules for those steps are defined here
# default if blank is 1 step with module type "solid" 
model = febio.Model(modelfile='test.feb',steps=[{'Displace': 'biphasic'}])

#initialize a list to store MatDef objects in
materials = []

#Create 3 MatDef objects with types biphasic, isotropic elastic, and rigid body and append them to mats list
materials.append(febio.MatDef(matid=1,mname='Biphasic',elsets='exmymzm',mtype='biphasic'))
materials.append(febio.MatDef(mname='Elastic',elsets='exmymzp',mtype='neo-Hookean',matid=2,attributes={'E': '1.0', 'v': '0.3'}))
materials.append(febio.MatDef(mname='Elastic 2',elsets='expymzm',mtype='neo-Hookean',matid=3,attributes={'E': '2.0','v': '0.3'}))

#Append additional element sets to elset attribute of MatDef objects
materials[0].appendElset('exmypzm')
materials[1].appendElset('exmypzp')
materials[2].appendElset('expypzm')
materials[2].appendElset('expypzp')
materials[2].appendElset('expymzp')

# Add a new subelement to material definitions: note how attributes are passed in a dictionary and all entries are strings
materials[0].addBlock(branch=1,btype='solid',mtype='neo-Hookean',attributes={'E': '1.0', 'v': '0.3'})
materials[0].addBlock(branch=1,btype='permeability',mtype='perm-const-iso',attributes={'perm': '1.0e-3'})

materials.append(febio.MatDef(mname='Plane',elsets='eplane',mtype='rigid body',matid=4,attributes={'density': '1.0'}))

for mat in materials:
    model.addMaterial(mat)
    
#add an element to the mesh
mesh.addElement(etype='quad4',corners=[0.,1.,0.,1.,1.,0.,1.,0.,0.,0.,0.,0.],name='plane')

#add element data
mesh.addElementData(elset='eplane',attributes={'thickness': '.01,.01,.01,.01'})


#Fill in the geometry block of model: THIS MUST FOLLOW MATERIAL DEFINITIONS for a working model
model.addGeometry(mesh=mesh,mats=materials)

# create a Control object with default values: this will always work this way
ctrl = febio.Control()

# change attributes you wish: dictionary keys must match FEBio's control parameters (not case-sensitive)
ctrl.setAttributes({'title': 'example'})

# Add Control block to first step block
model.addControl(ctrl,step=0)

# Define boundary conditions
boundary = febio.Boundary(steps=1)
boundary.addFixed(nset=mesh.nsets['nxp'],dof='xyz')
boundary.addPrescribed(step=0,nset=mesh.nsets['nxm'],dof='x',lc='1',scale='0.1')
boundary.addContact(step=0,ctype='rigid',master=4,slave=mesh.nsets['nzm'])

#Add rigid body constraint
model.addConstraint(matid=4,dof={'trans_z': 'fixed','rot_x': 'fixed','rot_y': 'fixed','rot_z': 'fixed'})

# Add boudary conditions to model
model.addBoundary(boundary=boundary)

# Add load curves to model
model.addLoadCurve(lc='1',lctype='smooth',points=[0,0,.5,.33,1,1])

#Write the model to file
model.writeModel()
