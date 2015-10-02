'''
Created on 2013-05-15

@author: Scott Sibole
'''

class MatDef(object):
    '''
    Define a material
    Member functions:
        addBlock(): add an xml block to the root material block
        
    '''

    def __init__(self,mtype=None,elsets=None,mname=None,matid=None,attributes=None):
        '''
        mtype = material type
        elset = element set to assign material to
        mname = material name
        '''
        if not matid:
            print "ERROR: You must specify a material id! Terminating execution..."
            raise SystemExit
        self.attributes = attributes
        self.matid = matid
        self.mtype = mtype
        if isinstance(elsets,list):
            self.elsets = elsets
        else:
            self.elsets = [elsets]
        self.mname = mname
        self.blocks = []
        #create the root material block
        self.addBlock(0,'material')
        
    def addBlock(self,branch=None,btype=None,mtype=None,attributes=None):
        '''
        Add block definition to list of blocks in material
        Order for list entry: branch level (0=root), block type (material,solid,fluid,etc.), matid (integer if root, False otherwise),
            material name (string if root, False otherwise), material type, dictionary of attributes or False if none
        '''
        if branch == 0:
            attributes = self.attributes
        blk = {'branch': branch,
               'btype': btype,
               'mtype': mtype,
               'attributes': attributes}
        
        self.blocks.append(blk)
        
    def appendElset(self,elset):
        self.elsets.append(elset)
        
        
