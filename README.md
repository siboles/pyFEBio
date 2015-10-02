# pyFEBio
A Python API for FEBio
Verification Scripts:
    febio/verification/body_force.py - static analysis of gravity body force
    febio/verification/body_force_time_dependent - static analysis of body force (gravity) decreasing with simulation time
    febio/verification/rigid_wall.py - model testing rigid_wall interface definition and using this to deform the block
    febio/verification/rigid_interface.py - model testing rigid interface contact definition and using this to deform the block; also tests adding an element to mesh manually
    febio/verification/sliding.py - model testing facet-to-facet sliding contact and manual element addition
    febio/verification/multi_step.py - model with 2 steps and prescribed nodal displacements (second step is relative)
