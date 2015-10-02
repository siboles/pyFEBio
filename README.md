# pyFEBio #
A Python API for FEBio
## Installation ##
In directory containing *setup.py*, type:
<pre><code> python setup.py install </code>
## Usage ##
To import the module:
<pre><code> import febio </code>

To construct an FEBio model file (.feb) using the classes in this module do the following:
1. Define a mesh by either importing an ABAQUS input file (only support for now) or by manually adding element, node, and set definitions.
<pre><code> mesh = febio.MeshDef("ABAQUS.inp", "ab") </code>
2. Create a model object.
<pre><code> model = febio.Model(modelfile="MODELNAME.feb", steps=[{"STEP1_NAME": "ANALYSIS_TYPE"}, {"STEP2_NAME": "ANALYSIS_TYPE"}, ...])</code>
3. Create material(s) defintion(s) and sets of elements to assign to.
<pre><code> mat = febio.MatDef(matid=MATERIAL_ID(TYPE=INT), mname="MATERIAL_NAME", mtype="MATERIAL_TYPE", elsets=["ELSET_NAME1",...], attributes={"MATERIAL_ATTRIBUTE1": "VALUE", ...})</code>
4. Add the geometry to the model object.
<pre><code> model.addGeometry(mesh=mesh, mats=[mat, ...])</code>
5. Create load curves to control loading and prescribed boundary conditions.
<pre><code>model.addLoadCurve(lc="ID_INT", lctype="LOAD_CURVE_TYPE", points=[time_0, value_0, ...])</code>
6. Create boundary conditions.
7. Create loads
8. Add boundary conditions to model.
9. Add loads to model.
10. Add a control block to model.

## Example Scripts ##
* febio/verification/body_force.py - static analysis of gravity body force
* febio/verification/body_force_time_dependent - static analysis of body force (gravity) decreasing with simulation time
* febio/verification/rigid_wall.py - model testing rigid_wall interface definition and using this to deform the block
* febio/verification/rigid_interface.py - model testing rigid interface contact definition and using this to deform the block; also tests adding an element to mesh manually
* febio/verification/sliding.py - model testing facet-to-facet sliding contact and manual element addition
* febio/verification/multi_step.py - model with 2 steps and prescribed nodal displacements (second step is relative)
