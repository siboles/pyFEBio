import febio

# create a MeshDef object, mesh, reading in simpleblock.inp in abaqus format
mesh = febio.MeshDef('simpleblock.inp','abq')

#add a shell element to the mesh
mesh.addElement(etype='quad4',corners=[0.,1.,1.,1.,1.,1.,1.,0.,1.,0.,0.,1.],name='plane')

#add element data for the shell
mesh.addElementData(elset='eplane',attributes={'thickness':'0.1,0.1,0.1,0.1'})

# create a Model obect, model, that will be written to test.feb
# NOTE: all steps and modules for those steps are defined here
# default if blank is 1 step with module type "solid" 
model = febio.Model(modelfile='sliding.feb',steps=[{'Displace': 'solid'}])

#make a material
mat1 = febio.MatDef(matid=1,mname='Material 1',mtype='neo-Hookean',elsets=['exmymzm','exmypzm','exmymzp','exmypzp','expymzm','expypzm','expymzp','expypzp'],attributes={'density': '1.0', 'E': '1.0','v': '0.3'})
mat2 = febio.MatDef(matid=2,mname='Rigid',mtype='rigid body',elsets='eplane',attributes={'density': '1.0'})

#add the materials to the model
model.addMaterial(mat1)
model.addMaterial(mat2)

#make the geometry section of the model
model.addGeometry(mesh=mesh,mats=[mat1,mat2])


#define a loadcurve
model.addLoadCurve(lc='1',lctype='linear',points=[0,0,1,1])

#initialize a boundary condition object
boundary = febio.Boundary(steps=1)

#add a rigid contact interface to boundary object
boundary.addContact(step=0,ctype='facet-to-facet sliding',main=mesh.fsets['fplane'],subordinate=mesh.fsets['fzp'],attributes={'penalty':'1000.0'})

#add a fixed boundary condition to nodes of top z face
boundary.addFixed(nset=mesh.nsets['nzm'],dof='xyz')

#add the boudary conditions to the model
model.addBoundary(boundary)

#add a rigid body constraints
model.addConstraint(step=0,matid=2,dof={'trans_x': 'fixed', 'trans_y': 'fixed', 'trans_z': ['prescribed','1','-0.1'], 'rot_x': 'fixed', 'rot_y': 'fixed', 'rot_z': 'fixed'}) 

#create a control block for step 1
ctrl = febio.Control()

#add the control block to the model
model.addControl(step=0,ctrl=ctrl)

#generate the model file
model.writeModel()
