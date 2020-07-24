'''
Created on 2013-05-15

@author: Scott Sibole
'''
from __future__ import print_function
from builtins import str
from builtins import map
from builtins import range
from builtins import object
import xml.etree.cElementTree as ET
import string
import itertools

class Model(object):
    '''
    Class defines and provides means for outputting the XML format .feb file
    Creating the object will initialize a skeleton of the model tree
    object_name = Model(self,vers='1.2',modelfile="default.feb",encode="ISO-8859-1",steps=[{'Step01': 'solid'}]):
        vers - febio spec version to use
        modelfile - name for .feb file to output
        encode - text encoding type (this likely should never be changed)
        steps - a list of dictionaries each entry defining a step
            dictionary structure: key (step name): item (module type)
            NOTE: there must always be 1 step
    Model information is then added by using the following member functions:
        addControl(self,ctrl=None,step=0): ctrl is a febio.Control object, step is an integer specifying which step to add control parameters to
        
        addOutput(self,output=None,): the output section of the XML file is initially populated with the default values for the module indicated in the first step
            additional output parameters can be added individually or as list e.g. output='nodal fluid flux' or output = ['nodal fluid flux','contact pressure']
            TODO: add support for logfile output including specified sets
        
        addMaterial(self,mat=None): mat is an febio.MatDef object
        
        addGeometry(self,mesh=None,mats=None): mesh is an febio.MeshDef object; mats is a list of febio.MatDef objects
        
        addLoadCurve(self,lc=None,lctype=None,points=[0,0,1,1]): add a loadcurve definition to the model points list is read in chunks of two and must be even in length
        
        addConstraint(self,step=0,matid=None,dof=None):
            step - integer step counter
            matid - rigid body material ID
            dof - the degrees of freedom to constrain in a dictionary e.g.
                {'trans_x': ['prescribed','1','1'], 'trans_y': ['force','1','1'], 'trans_z': 'fixed'}
                NOTE: for prescribed or force constraints list must be 3 elements and ordered as TYPE, LOADCURVE ID, SCALE FACTOR; for 'fixed' constraint assigned string 'fixed' not as a list
        
        addGlobal(self,constants=None,solutes=None,generations=None):
            constants - dictionary with keys being the XML tag for each constant and items being value
            solutes - dictionary with keys being the name for each solute items are the value
            globals - list of generation values
        
        writeModel(self): when called writes the XML tree to modelfile specified during febio.Model object creation (default = 'default.feb')
        
        __indent(self): private function used to recursively indent and carriage return the XML tree so it is more human-readable      
    '''


    def __init__(self,vers='1.2',modelfile="default.feb",encode="ISO-8859-1",steps=[{'Step01': 'solid'}]):
        '''
        Constructor
        '''
        self.modelfile = modelfile
        self.encode = encode
        self.root = ET.Element("febio_spec",version=vers)
        self.material = ET.SubElement(self.root,"Material")
        self.geometry = ET.SubElement(self.root,"Geometry")
        self.nodes = ET.SubElement(self.geometry,"Nodes")
        self.elements = ET.SubElement(self.geometry,"Elements")
        self.output = ET.SubElement(self.root,"Output")
        self.plotfile = ET.SubElement(self.output,"plotfile",type="febio")
        self.initialBoundary = ET.SubElement(self.root,'Boundary')
        self.initialConstraint = ET.SubElement(self.root,"Constraints")
        self.steps = []
        self.boundary = []
        self.constraint = []
        self.load = []
        cnt = 0
        for i in steps:
            self.steps.append(ET.SubElement(self.root,"Step", name=list(i.keys())[0]))
            ET.SubElement(self.steps[cnt],"Module", type=i[list(i.keys())[0]])
            self.boundary.append(ET.SubElement(self.steps[cnt],"Boundary"))
            self.load.append(ET.SubElement(self.steps[cnt],"Loads"))
            self.constraint.append(ET.SubElement(self.steps[cnt],"Constraints"))
            cnt += 1
        
        #Set default output variables depending on module of first step
        mod = steps[0][list(steps[0].keys())[0]]
        if mod == 'solid':
            ET.SubElement(self.plotfile,"var",type="displacement")
            ET.SubElement(self.plotfile,"var",type="stress")
        elif mod == 'biphasic' or mod == 'poro':
            ET.SubElement(self.plotfile,"var",type="displacement")
            ET.SubElement(self.plotfile,"var",type="stress")
            ET.SubElement(self.plotfile,"var",type="effective fluid pressure")
            ET.SubElement(self.plotfile,"var",type="fluid flux")
        else:
            print('ERROR: Sorry the '+mod+' module is not supported at this time. Terminating execution...')
            raise SystemExit
            
        
    def addControl(self,ctrl=None,step=0):
        step_ctrl = ET.SubElement(self.steps[step],"Control")
        for i in list(ctrl.attributes.keys()):
            if ctrl.attributes[i] is not None:
                if i == 'linear_solver' or i=='analysis':
                    ET.SubElement(step_ctrl,i,type = ctrl.attributes[i])
                elif i == 'time_stepper':
                    dmy = ET.SubElement(step_ctrl,i)
                    for j in list(ctrl.attributes[i].keys()):
                        if j == 'dtmax' and 'lc' in ctrl.attributes[i][j] :
                            ET.SubElement(dmy, j, lc=ctrl.attributes[i][j].replace("lc=", ""))
                        else:
                            ET.SubElement(dmy,j).text = ctrl.attributes[i][j]        
                else:
                    ET.SubElement(step_ctrl,i).text = ctrl.attributes[i]
                
    def addOutput(self,output=None):
        if output is not None:
            if isinstance(output, list):
                for i in output:
                    ET.SubElement(self.plotfile,"var",type=i)
            else:
                ET.SubElement(self.plotfile,"var",type=output)
            
       
    def addMaterial(self,mat=None):
        if mat is not None:
            levels = []
            for blk in mat.blocks:
                level = blk['branch']
                if level == 0:
                    dmy = ET.SubElement(self.material,blk['btype'],id=str(mat.matid),name=mat.mname,type=mat.mtype)
                    levels.append(dmy)
                    if blk['attributes'] is not None:
                        for i in list(blk['attributes'].keys()):
                            if isinstance(blk['attributes'][i], list):
                                if 'vector' == blk['attributes'][i][0]:
                                    dmy2 = ET.SubElement(dmy, i, type=blk['attributes'][i][0])
                                    ET.SubElement(dmy2, "a").text = blk['attributes'][i][1]
                                    ET.SubElement(dmy2, "d").text = blk['attributes'][i][2]
                                else:
                                    ET.SubElement(dmy,i,type=blk['attributes'][i][0]).text = blk['attributes'][i][1]
                            else:    
                                ET.SubElement(dmy,i).text = blk['attributes'][i]
                    continue
                elif level > len(levels) - 1:
                    dmy = ET.SubElement(levels[level-1],blk['btype'])
                    levels.append(dmy)
                else:
                    dmy = ET.SubElement(levels[level-1],blk['btype'])
                if blk['mtype'] is not None:
                    dmy.attrib['type'] = blk['mtype']
                    
                if blk['attributes'] is not None:
                    for i in list(blk['attributes'].keys()):
                        if isinstance(blk['attributes'][i], list):
                            if 'vector' == blk['attributes'][i][0]:
                                dmy2 = ET.SubElement(dmy, i, type=blk['attributes'][i][0])
                                ET.SubElement(dmy2, "a").text = blk['attributes'][i][1]
                                ET.SubElement(dmy2, "d").text = blk['attributes'][i][2]
                            else:
                                ET.SubElement(dmy,i,type=blk['attributes'][i][0]).text = blk['attributes'][i][1]
                        else:
                            ET.SubElement(dmy,i).text = blk['attributes'][i]

    
    def addGeometry(self,mesh=None,mats=None):
        if mesh is not None:
            if mats is not None:
                for i in range(len(mesh.nodes)):
                    ET.SubElement(self.nodes, "node", id=str(i + 1)).text = (
                        ",".join(list(map(str, mesh.nodes[i][1:]))))
                '''

                for i, e in enumerate(mesh.elements):
                    for m in mats:
                        for es in m.elsets:
                            if e[1] in mesh.elsets[es]:
                                #mesh.elsets[es][e[1]]
                                matid = m.matid
                                break
                        else:
                            continue
                        break
                    ET.SubElement(self.elements,e[0],id=str(i+1),mat=str(matid)).text = string.join(map(str,mesh.elements[i][2:]),',')
                '''

                matids = [0] * len(mesh.elements)
                for i, m in enumerate(mats):
                    for es in m.elsets:
                        for e in mesh.elsets[es]:
                            matids[e - 1] = m.matid
                for i, e in enumerate(mesh.elements):
                    text = ",".join(list(map(str, mesh.elements[i][2:])))
                    ET.SubElement(self.elements, e[0], id=str(i + 1), mat=str(matids[i])).text = text

            if mesh.elementdata:
                self.elementdata = ET.SubElement(self.geometry,"ElementData")
                for i in list(mesh.elementdata.keys()):
                    dmy = ET.SubElement(self.elementdata,"element",id=str(i))
                    for j in mesh.elementdata[i]:
                        ET.SubElement(dmy,list(j.keys())[0]).text = j[list(j.keys())[0]]              
                
        else:
            print('WARNING: No Geometry added. You need to specify a mesh and/or material object')

            
    
    def addBoundary(self,boundary=None):
        if boundary is not None:
            self.prescribedblk = []
            self.prescribedrelblk = []
            self.contactblk = []
            self.springblk = []
            for i in range(len(boundary.bcs)):
                step = boundary.bcs[i]        
                if len(step['fixed']) > 0:
                    self.fixedblk = ET.SubElement(self.initialBoundary,'fix')
                    for b in step['fixed']:
                        ET.SubElement(self.fixedblk,'node',id=str(b[0]),bc=str(b[1]))
                if len(step['prescribed']) > 0:
                    self.prescribedblk.append(ET.SubElement(self.boundary[i],'prescribe'))
                    for b in step['prescribed']:
                        ET.SubElement(self.prescribedblk[-1],'node',id=str(b[0]),bc=str(b[1]),lc=str(b[2])).text = str(b[3])
                if len(step['prescribed relative']) > 0:
                    self.prescribedrelblk.append(ET.SubElement(self.boundary[i],'prescribe',type='relative'))
                    for b in step['prescribed relative']:
                        ET.SubElement(self.prescribedrelblk[-1],'node',id=str(b[0]),bc=str(b[1]),lc=str(b[2])).text = str(b[3])
                if len(step['contact']) > 0:
                    cnt = 0
                    for c in step['contact']:
                        self.contactblk.append(ET.SubElement(self.boundary[i],'contact',type=c['type']))
                        if c['attributes'] is not None:
                            for a in list(c['attributes'].keys()):
                                ET.SubElement(self.contactblk[cnt],a).text = c['attributes'][a]
                        if c['type']=='rigid':
                            for n in c['subordinate']:
                                ET.SubElement(self.contactblk[cnt],"node",id=str(n),rb=str(c['main']))
                        elif 'sliding' in c['type'] or 'tied' in c['type'] or 'periodic' in c['type']:
                            dmy = ET.SubElement(self.contactblk[cnt],"surface",type="main")
                            for f in c['main']:
                                ET.SubElement(dmy,f[0],id=str(f[1])).text = ",".join(list(map(str,f[2:])))
                            dmy = ET.SubElement(self.contactblk[cnt],"surface",type="subordinate")
                            for f in c['subordinate']:
                                ET.SubElement(dmy,f[0],id=str(f[1])).text = ",".join(list(map(str,f[2:])))
                        elif c['type']=='rigid_wall':
                            ET.SubElement(self.contactblk[-1],"plane",lc=str(c['main'][0])).text = ",".join(list(map(str,c['main'][1:])))
                            dmy = ET.SubElement(self.contactblk[cnt],"surface",type="subordinate")
                            for f in c['subordinate']:
                                ET.SubElement(dmy,f[0],id=str(f[1])).text = ",".join(list(map(str,f[2:])))
                        cnt += 1
                if len(step['spring']) > 0:
                    for b in step['spring']:
                        if b['stype'] == 'linear':
                            self.springblk.append(ET.SubElement(self.initialBoundary,'spring',type=b['stype']))
                            ET.SubElement(self.springblk[-1],'node').text=str(b['n1'])+','+str(b['n2'])
                            ET.SubElement(self.springblk[-1],'E').text=str(b['E'])

    
    def addLoad(self,load=None):
        if load is not None:
            self.forceblk = []
            self.pressureblk = []
            self.tractionblk = []
            self.ffluxblk = []
            self.sfluxblk = []
            self.bfblk = []
            for i in range(len(load.loads)):
                step = load.loads[i]
                if len(step['force']) > 0:
                    self.forceblk.append(ET.SubElement(self.load[i],"force"))
                    for f in step['force']:
                        ET.SubElement(self.forceblk[-1],"node",id=str(f[0]),bc=str(f[1]),lc=str(f[2])).text = str(f[3])
                                
                if len(step['pressure']) > 0:
                    cnt = 0
                    for p in step['pressure']:
                        self.pressureblk.append(ET.SubElement(self.load[i],"pressure"))
                        for s in p['surface']:
                            ET.SubElement(self.pressureblk[cnt],s[0],id=str(s[1]),lc=p['lc'],scale=p['scale']).text = ",".join(list(map(str,s[2:])))
                        cnt += 1
                
                if len(step['normal_traction']) > 0:
                    cnt = 0
                    for t in step['normal_traction']:
                        self.tractionblk.append(ET.SubElement(self.load[i],"normal_traction",traction=t['traction']))
                        for s in t['surface']:
                            ET.SubElement(self.tractionblk[cnt],s[0],id=str(s[1]),lc=t['lc'],scale=t['scale']).text = ",".join(list(map(str,s[2:])))
                        cnt += 1
                        
                if len(step['fluidflux']) > 0:
                    cnt = 0
                    for ff in step['fluidflux']:
                        self.ffluxblk.append(ET.SubElement(self.load[i],"fluidflux",type=ff['type'],flux=ff['flux']))
                        for s in ff['surface']:
                            ET.SubElement(self.ffluxblk[cnt],s[0],id=str(s[1]),lc=ff['lc'],scale=ff['scale']).text = ",".join(list(map(str,s[2:])))
                        cnt += 1
                                             
                if len(step['soluteflux']) > 0:
                    cnt = 0
                    for sf in step['soluteflux']:
                        self.sfluxblk.append(ET.SubElement(self.load[i],"soluteflux",type=sf['type'],sol=sf['sol']))
                        for s in sf['surface']:
                            ET.SubElement(self.sfluxblk[cnt],s[0],id=str(s[1]),lc=sf['lc'],scale=sf['scale']).text = ",".join(list(map(str,s[2:])))
                        cnt += 1

                if len(step['body_force']) > 0:
                    cnt = 0
                    for bf in step['body_force']:
                        self.bfblk.append(ET.SubElement(self.load[i],"body_force",type=bf['type']))
                        for a in list(bf['attributes'].keys()):
                            if isinstance(bf['attributes'][a],list):
                                ET.SubElement(self.bfblk[cnt],a,lc=bf['attributes'][a][0]).text = str(bf['attributes'][a][1])
                            else:
                                ET.SubElement(self.bfblk[cnt],a).text = str(bf['attributes'][a])
                                                                   
    def addConstraint(self,step=None,matid=None,dof=None):
        if matid is None:
            print("WARNING: No material ID was specified.  Skipping constraint definition...")
            pass
        if dof is None:
            print("WARNING: No degree(s) of freedom was specified.  Skipping constraint definition...")
            pass
        if step is None:
            parent = ET.SubElement(self.initialConstraint,"rigid_body",mat=str(matid))
        else:
            parent = ET.SubElement(self.constraint[step],"rigid_body",mat=str(matid))
        for i in list(dof.keys()):
            if isinstance(dof[i],list):
                try:
                    ET.SubElement(parent,i,type=dof[i][0],lc=dof[i][1]).text = dof[i][2]
                except:
                    print("WARNING: When defining a force or prescribed constraint the list must be 3 elements long and ordered: TYPE, LOADCURVE ID, SCALE FACTOR.  Skipping definition...")
            else:
                ET.SubElement(parent,i,type=dof[i])

                    
    def addLoadCurve(self,lc=None,lctype=None,points=[0,0,1,1]):
        try:
            self.loaddata
        except:
            self.loaddata = ET.SubElement(self.root,"LoadData")
        if lc is None:
            print("WARNING: No load curve id specified. Assuming default value of 1...")
            lc = '1'
        if lctype is None:
            print("WARNING: No load curve type specified. Assuming default value of linear")
        if len(points)%2 > 0:
            print("ERROR: There must be an even number of load curve points.  Terminating execution...")
            raise SystemExit
        dmy = ET.SubElement(self.loaddata,"loadcurve",id=lc,type=lctype)
        for i in range(0,len(points),2):
            ET.SubElement(dmy,'loadpoint').text = str(points[i])+','+str(points[i+1])
            
    def addGlobal(self,constants=None, solutes=None, generations=None):
        try:
            self.globals
        except:
            self.globals = ET.SubElement(self.root,"Globals")
        if constants is not None:
            try:
                for i in list(constants.keys()):
                    ET.SubElement(self.constants,i).text = str(constants[i])
            except:
                self.constants = ET.SubElement(self.globals,"Constants")
                for i in list(constants.keys()):
                    ET.SubElement(self.constants,i).text = str(constants[i])
                    
        if solutes is not None:
            try:
                cnt = len(self.solutes)
                for i in list(solutes.keys()):
                    ET.SubElement(self.solutes,"solute",id=str(cnt),name=i).text = str(solutes[i])
                    cnt += 1
            except:
                cnt = 1
                self.solutes = ET.SubElement(self.globals,"Solutes")
                for i in list(solutes.keys()):
                    ET.SubElement(self.solutes,"solute",id=solutes[i][0],name=i).text = str(solutes[i][1])
                    cnt += 1
                    
        if generations is not None:
            try:
                cnt = len(self.generations)
                for i in generations:
                    ET.SubElement(self.generations,"gen",id=str(cnt)).text = str(i)
                    cnt += 1
            except:
                cnt = 1
                self.generations = ET.SubElement(self.globals, "Generations")
                for i in generations:
                    ET.SubElement(self.generations,"gen",id=str(cnt)).text = str(i)
                    cnt += 1
                
                    
                    
            
    def writeModel(self):
        
        # Assemble XML tree
        tree = ET.ElementTree(self.root)
        
        # Make pretty format
        level = 0
        elem = tree.getroot()
        self.__indent(elem,level)
        
        #Write XML file
        tree.write(self.modelfile,encoding=self.encode)
        
        
        
    def __indent(self,elem,level):
        i = '\n' + level*'  '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + '  '
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for child in elem:
                    self.__indent(child, level+1)
                if not child.tail or not child.tail.strip():
                    child.tail = i
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
