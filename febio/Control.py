'''
Created on 2013-05-15

@author: Scott Sibole
'''
import string

class Control(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #Defaults values
        self.attributes = {'title': None,
                           'time_steps': '10',
                           'step_size': '0.1',
                           'dtol': '0.001',
                           'etol': '0.01',
                           'rtol': '0',
                           'lstol': '0.9',
                           'time_stepper': {'dtmin': '0.01', 'dtmax': '1', 'max_retries': '10', 'opt_iter': '10'},
                           'max_refs': '15',
                           'max_ups': '10',
                           'optimize_bw': '0',
                           'restart': '0',
                           'plot_level': 'PLOT_MAJOR_ITRS',
                           'cmax': '1e5',
                           'analysis': 'static',
                           'print_level': 'PRINT_MINOR_ITRS',
                           'min_residual': '1e-20',
                           'integration': None
                           }
    def setAttributes(self,specified):
        for i in specified.keys():
            self.attributes[string.lower(i)] = specified[i]
            
            
        
