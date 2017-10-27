'''
Created on 2013-05-15

@author: Scott Sibole
'''
from __future__ import print_function
from builtins import range
from builtins import object

class Boundary(object):
    '''
    classdocs
    '''

    def __init__(self,steps=1):
        '''
        self.bcs - list of Dictionaries containing all boundary conditions with the following types
            fixed - list with each entry containing a 2 element list of: node id, dof
            prescribed - list with each entry containing a 4 element list of: node id, dof, load curve id, scale
            prescribed relative - same as prescribed but has type relative (relative BCs have to have a separate XML parent)
            contact - list containing a dictionaries each containing
                ctype - 'sliding_with_gaps', 'facet-to-facet sliding', 'sliding2', 'sliding3', 'rigid', 'rigid_wall', 'tied', 'tied-biphasic', 'sliding-tension-compression'
                master - master node or surface set (MeshDef.nset or MeshDef.fset attribute) OR if rigid: the rigid body id; if rigid_wall: the plane equation
                slave - slave node or surface set
                attributes - any attributes that should be specified: pass as a dictionary {attribute tag: value}
            spring - list with each entry containing a 6 element list of: type, node 1, node 2, E, force load curve id, scale
        '''
        self.bcs = []
        for _ in range(steps):
            self.bcs.append({'fixed': [], 'prescribed': [], 'prescribed relative': [], 'contact': [],'spring': []})
        
    def addFixed(self,nset=None,nodeid=None,dof=None):        
        if dof is None:
            print('WARNING: No degree of freedom was specified for this boundary condition.  Skipping...')
            pass
        
        if nset is None and nodeid is None:
            print('WARNING: Must specify either a node set or a node id.  Skipping...')
            pass
            
        if nset is not None:
            for n in nset:
                self.bcs[0]['fixed'].append([n,dof])
                
        if nodeid is not None:
            if isinstance(nodeid, list):
                for n in nodeid:
                    self.bcs[0]['fixed'].append([n,dof])
            else:
                self.bcs[0]['fixed'].append([nodeid,dof])
            
    
    def addPrescribed(self,nset=None,step=0,nodeid=None,dof=None,lc=None,scale=None,ptype=None):
        if dof is None:
            print('WARNING: No degree of freedom was specified for this boundary condition.  Skipping BC assignment...')
            pass
        
        if nset is None and nodeid is None:
            print('WARNING: Must specify either a node set or a node id.  Skipping BC assignment...')
            pass
        
        if lc is None:
            print('WARNING: Must specify a load curve ID. Skipping BC assignment...')
            pass
        
        if scale is None:
            print('WARNING: No scale specified for this boundary condition.  Using default of 1.0...')
            scale = 1.0
        if ptype is not None:
            keywd = 'prescribed relative'
        else:
            keywd = 'prescribed'
        
        if nset is not None:
            for n in nset:
                self.bcs[step][keywd].append([n,dof,lc,scale])
                
        if nodeid is not None:
            if isinstance(nodeid, list):
                for n in nodeid:
                    self.bcs[step][keywd].append([n,dof,lc,scale])
            else:
                self.bcs[step][keywd].append([nodeid,dof,lc,scale])
    
    def addContact(self,step=0,ctype=None,master=None,slave=None,attributes=None):
        if ctype is None:
            print('WARNING: Did not specify a contact type. Skipping assignment...')
            pass
        
        elif master is None or slave is None:
            print('WARNING: Did not specify an appropriate value for the master and/or slave.  Skipping assignment...')
            pass
        try:
            if isinstance(master[0][0],list):
                dmy = []
                for i in master:
                    for j in i:
                        dmy.append(j)
                master = dmy
        except:
            master = master
        try:
            if isinstance(slave[0][0],list):
                dmy = []
                for i in slave:
                    for j in i:
                        dmy.append(j)
                slave = dmy
        except:
            slave = slave
        self.bcs[step]['contact'].append({'type': ctype, 'master': master, 'slave': slave, 'attributes': attributes})    
        
    def addSpring(self,step=0,stype='linear',nodes=[None,None],E=None,lc=None,scale=1.0):
        if len(nodes) != 2 or not isinstance(nodes[0],int) or not isinstance(nodes[1],int):
            print('WARNING: List of nodes must be 2 integer elements.  Skipping spring definition...')
            pass
        if stype=='linear' or stype=='tension-only nonlinear':
            if E is None:
                print('WARNING: Must specify a spring stiffness if type is linear or tension-only linear.  Skipping spring definition...')
                pass
        if stype=='nonlinear' and lc is None:
            print('WARNING: Must specify a force load curve if type is nonlinear.  Skipping spring definition...')
            pass
        if stype=='nonlinear' and scale is None:
            print('WARNING: No scale was specified.  Using default value of 1.0...')
            scale = 1.0 
        
        self.bcs[step]['spring'].append({'stype':stype,'n1':nodes[0],'n2':nodes[1],'E':E,'lc':lc,'scale':scale})
        
        
        
        
            
        
