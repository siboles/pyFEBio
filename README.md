# NO LONGER MAINTAINED -- FOR AN ACTIVELY SUPPORTED ALTERNATIVE SEE:
https://github.com/febiosoftware/pyfebio

# pyFEBio #
A Python API for FEBio
## Installation ##
In directory containing *setup.py*, type:
<pre><code> python setup.py install </code></pre>
## Usage ##
To import the module
<pre><code> import febio </code></pre>

To construct an FEBio model file (.feb) using the classes in this module, do the following:

1. Define a mesh by either importing an ABAQUS input file (only support for now) or by manually adding element, node, and set definitions.
2. Create a model object.
3. Create material(s) defintion(s) and sets of elements to assign to.
4. Add the geometry to the model object.
5. Add load curves to control loading and prescribed boundary conditions.
6. Create boundary conditions, loads, constraints, and contact defitions.
7. Add boundary condition, load, constraint, and contact objects to model object.
8. Create a control object.
9. Set the attributes of the control object you wish to modify from default.
10. Add the control object to model object.
11. Write the model to disk.

## Example Scripts ##
* febio/verification/body_force.py - static analysis of gravity body force
* febio/verification/body_force_time_dependent - static analysis of body force (gravity) decreasing with simulation time
* febio/verification/rigid_wall.py - model testing rigid_wall interface definition and using this to deform the block
* febio/verification/rigid_interface.py - model testing rigid interface contact definition and using this to deform the block; also tests adding an element to mesh manually
* febio/verification/sliding.py - model testing facet-to-facet sliding contact and manual element addition
* febio/verification/multi_step.py - model with 2 steps and prescribed nodal displacements (second step is relative)

## Planned Changes ##
The class structure of this module is poorly conceived due to each class being orphaned. In the future, it will be entirely restructured using inheritance to make model generation much more convenient. 
