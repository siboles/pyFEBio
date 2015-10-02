'''
Created on 2013-05-21

@author: Scott Sibole
'''

class Load(object):
    '''
    self.loads - list of dictionaries with keys holding lists of all load types assigned in a given step
        'force' - append to this list with addForce()
        'pressure' - append to this list with addPressure()
        'normal_traction' - append to this list with addTraction()
        'fluidflux' - append to this list with addFluidFlux()
        'soluteflux' - append to this list with addSoluteFlux()
        'body_force' - append to this list with addBodyForce()
    '''
    
    def __init__(self,steps=1):
        '''
        Constructor
        '''
        self.loads = []
        for _ in xrange(steps):
            self.loads.append({'force': [], 'pressure': [], 'normal_traction': [], 'fluidflux': [], 'soluteflux': [], 'body_force': []})
            
    def addForce(self,step=0,nset=None,nodeid=None,dof=None,lc=None,scale=None):
        if dof is None:
            print 'WARNING: No degree of freedom was specified for this nodal force.  Skipping assignment...'
            pass
        
        if nset is None and nodeid is None:
            print 'WARNING: Must specify either a node set or a node id.  Skipping BC assignment...'
            pass
        
        if lc is None:
            print 'WARNING: No load curve ID specified for nodal force. Assuming load curve ID of 1...'
            pass
        
        if scale is None:
            print 'WARNING: No scale specified for nodal force.  Using default of 1.0...'
            scale = '1.0'
        
        if nset is not None:
            for n in nset:
                self.loads[step]['force'].append([n,dof,lc,scale])
                
        if nodeid is not None:
            if isinstance(nodeid, list):
                for n in nodeid:
                    self.loads[step]['force'].append([n,dof,lc,scale])
            else:
                self.loads[step]['force'].append([nodeid,dof,lc,scale])
    
    def addPressure(self,step=0,surface=None,lc=None,scale=None):
        if surface is None:
            print 'WARNING: Must specify surface as a MeshDef.fset object. Skipping pressure assignment...'
            pass
        if lc is None:
            print 'WARNING: No load curve ID specified for pressure.  Assuming load curve ID of 1...'
            lc = '1'
        if scale is None:
            print 'WARNING: No scale factor specified for pressure.  Assuming scale factor of 1.0...'
            scale = '1.0'
            
        self.loads[step]['pressure'].append({'lc': lc, 'scale': scale, 'surface': surface})
    
    def addTraction(self,step=0,surface=None,traction=None,lc=None,scale=None):
        if surface is None:
            print 'WARNING: Must specify surface as a MeshDef.fset object. Skipping prescribed traction assignment...'
            pass
        if traction is None:
            print 'WARNING: No traction type specified.  Assuming "mixture"...'
            traction = 'mixture'
        if lc is None:
            print 'WARNING: No load curve ID specified for prescribed traction. Assuming load curve ID of 1...'
            lc = '1'
        if scale is None:
            print 'WARNING: No scale factor specified for prescribed traction.  Assuming scale factor of 1.0...'
            scale = '1.0'
            
        self.loads[step]['normal_traction'].append({'traction': traction,'lc': lc, 'scale': scale, 'surface': surface})
    
    def addFluidFlux(self,step=0,method=None,surface=None,fluxtype=None,lc=None,scale=None):
        if method is None:
            print 'WARNING: No method specified for flux condition. Assuming to be "nonlinear"...'
            method = 'nonlinear'
        if surface is None:
            print 'WARNING: Must specify surface as a MeshDef.fset object. Skipping flux condition assignment...'
            pass
        if fluxtype is None:
            print 'WARNING: No fluxtype was specified.  Assuming to be "fluid"'
            fluxtype = 'fluid'
        if lc is None:
            print 'WARNING: No load curve specified for flux condition. Assuming load curve as 1...'
            lc = '1'
        if scale is None:
            print 'WARNING: No scale factor specified for flux condition. Assuming scale factor as 1.0...'
            scale = '1.0'
            
        self.loads[step]['fluidflux'].append({'type': method, 'flux': fluxtype, 'lc': lc, 'scale': scale, 'surface': surface})
    
    def addSoluteFlux(self,step=0,method=None,surface=None,solute=None,lc=None,scale=None):
        if method is None:
            print 'WARNING: No method specified for flux condition. Assuming to be "nonlinear"...'
            method = 'nonlinear'
        if surface is None:
            print 'WARNING: Must specify surface as a MeshDef.fset object. Skipping flux condition assignment...'
            pass
        if lc is None:
            print 'WARNING: No load curve specified for flux condition. Assuming load curve as 1...'
            lc = '1'
        if scale is None:
            print 'WARNING: No scale factor specified for flux condition. Assuming scale factir as 1.0...'
            scale = '1.0'
        self.loads[step]['fluidflux'].append({'type': method, 'sol': solute, 'lc': lc, 'scale': scale, 'surface': surface})
        
    def addBodyForce(self,step=0,btype=None,attributes=None):
        if btype is None:
            print "WARNING: Must specify a body force type.  Skipping assignment..."
            pass
        if attributes is None:
            print "WARNING: No attributes specified for body force.  Skipping assignment..."
            pass
        
        self.loads[step]['body_force'].append({'type': btype, 'attributes': attributes})