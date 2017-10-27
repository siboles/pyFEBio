'''
Created on 2013-05-15

@author: Scott Sibole
'''
from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import map
from builtins import range
from builtins import object
from past.utils import old_div
import numpy as np

class MeshDef(object):
    '''
    Class to store element, node, and set definitions
    Can parse Abaqus Input or HDF5 formats
    '''
    facetID = 1 #counter to assign unique IDs to surface facets defined in sets

    def __init__(self,mfile=None,mformat='manual',scale=[1.0,1.0,1.0]):
        '''
        '''
        self.mfile = mfile
        self.mformat = mformat
        self.elements = []
        self.nodes = []
        self.scale = list(map(float,scale))
        self.elsets = {}
        self.nsets = {}
        self.fsets = {}
        
        self.elementdata = {}
        if self.mfile is not None:
            self.parseMesh()
        
    def parseMesh(self):
        if self.mformat.lower() == 'abq':
            with open(self.mfile) as f:
                lines = [line.strip() for line in f]
            content = {}
            kywd =''
            kywds = []
            repeats = 0
            for line in lines:
                if '**' in line:
                    continue
                elif '*' in line:
                    kywd = line.lower()
                    try:
                        content[kywd]
                        kywd = kywd+str(repeats)
                        repeats += 1
                        content[kywd] = []
                        kywds.append(kywd)
                        continue
                    except:
                        content[kywd] = []
                        kywds.append(kywd)
                        continue
                dmy = [d.lower() for d in line.split(',')]
                try:
                    dmy.remove('')
                except:
                    pass
                content[kywd].append(dmy)
                
            for i in kywds:
                if 'node' in i:
                    for n in content[i]:
                        self.nodes.append([int(n[0])]+self.__scaleNode(list(map(float,n[1:]))))
                elif 'element' in i:
                    dmy = i.partition('type=')[-1]
                    if 'c3d8' in dmy:
                        etype = 'hex8'
                    elif 'c3d4' in dmy:
                        etype = 'tet4'
                    elif 'c3d6' in dmy:
                        etype = 'penta6'
                    elif 'cpe3' in dmy:
                        etype = 'tri3'
                    elif 'cpe4' in dmy:
                        etype = 'quad4'
                    else:
                        print("WARNING: Element type "+dmy+" is not supported. This section will be ignored...")
                        continue
                    for e in content[i]:
                        self.elements.append([etype]+list(map(int,e)))
                elif 'elset' in i:
                    setname = i.partition('=')[-1]
                    self.elsets[setname] = {}
                    for line in content[i]:
                        for e in line:
                            self.elsets[setname][int(e)] = True
                elif 'nset' in i:
                    setname = i.partition('=')[-1]
                    self.nsets[setname] = []
                    for line in content[i]:
                        for n in line:
                            self.nsets[setname].append(int(n))
                elif 'surface' in i:
                    setname = i.partition('=')[-1]
                    self.fsets[setname] = []
                    face_def = {
                                'hex8': {'s1': ['quad4',0,3,2,1], 's2': ['quad4',4,5,6,7], 's3': ['quad4',0,1,5,4], 's4': ['quad4',1,2,6,5], 's5': ['quad4',2,3,7,6],'s6': ['quad4',0,4,7,3]},
                                'tet4': {'s1': ['tri3',0,1,2], 's2': ['tri3',0,3,1], 's3': ['tri3',1,3,2], 's4': ['tri3',2,3,0]},
                                'penta6': {'s1': ['tri3',0,2,1], 's2': ['tri3',3,4,5], 's3': ['quad4',0,1,4,3], 's4': ['quad4',1,2,5,4], 's5': ['quad4',0,3,5,2]},
                                }
                    
                    for line in content[i]:
                        eid = int(line[0])
                        try:
                            elm = self.elements[eid-1]
                        except:
                            print(eid-1)
                        node_order = face_def[elm[0]][line[1]][1:]
                        stype = face_def[elm[0]][line[1]][0]
                        dmy = [stype,MeshDef.facetID]
                        for n in node_order:
                            dmy.append(elm[n+2])
                        self.fsets[setname].append(dmy)
                        MeshDef.facetID += 1
                else:
                    print('Mesh parser ignored keyword line: '+i)
                    
        elif self.mformat.lower() == 'hdf5':
            pass
        
    def addElementSet(self,setname=None,eids=None):
        if setname is None:
            print("WARNING: Must provide a setname. Skipping set generation...")
            pass
        if eids is None:
            print("WARNING: Did not specify any element IDs.  Skipping set generation...")
            pass
        
        self.elsets[setname] = {}
        for e in eids:
            self.elsets[setname][int(e)] = True
            
    def __scaleNode(self,node):
        return [node[0]*self.scale[0],node[1]*self.scale[1],node[2]*self.scale[2]]
    
    def addElement(self,etype='hex8',corners=[-1.0,-1.0,-1.0,1.,-1.0,-1.0,1.0,1.0,-1.0,-1.0,1.0,-1.0,-1.0,-1.0,1.0,1.0,-1.0,1.0,1.0,1.0,1.0,-1.0,1.0,1.0],name='new_elem'):
        '''
        corners - list of nodal coordinates properly ordered for element type (counter clockwise)
        '''
        lastelm = self.elements[-1][1]
        lastnode = self.nodes[-1][0]
        elm = [etype,lastelm+1]
        for i in range(old_div(len(corners),3)):
            elm.append(lastnode+1+i)
            
        self.elements.append(elm)
        self.elsets['e'+name] = {}
        self.elsets['e'+name][int(elm[1])] = True
        
        cnt = 1
        self.nsets['n'+name] = []
        for i in range(0,len(corners),3):
            self.nodes.append([lastnode+cnt, corners[i], corners[i+1], corners[i+2]])
            self.nsets['n'+name].append(lastnode+cnt)
            cnt += 1
        
        # if this is a quad4 or tri3 element make a surface set
        if etype == 'quad4' or etype == 'tri3':
            self.fsets['f'+name] = [[etype, MeshDef.facetID, lastnode+1, lastnode+2, lastnode+3, lastnode+4]]
            MeshDef.facetID += 1
    
    def addElementData(self,elset=None,eid=None,attributes=None):
        if elset is not None:
            for e in self.elsets[elset]:
                try:
                    self.elementdata[e].append(attributes)
                except:
                    self.elementdata[e] = []
                    self.elementdata[e].append(attributes)
        if eid is not None:
            try:
                self.elementdata[eid].append(attributes)
            except:
                self.elementdata[eid] = []
                self.elementdata[eid].append(attributes)
