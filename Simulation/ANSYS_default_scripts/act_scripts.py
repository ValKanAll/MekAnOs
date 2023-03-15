act_script_createMesh_default = \
r"""mesh_save_path = r"{mesh_save_path}"
nb_elem = {nb_elem} * 1000
size_elem = {size_elem}  # Approximate size of elements in mm (may be None if nb_elem is not None)
type_elem = "{type_elem}"  # Type of element. Either 'tet', 'hex' or 'voxel'.

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection


# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

if type_elem == 'QT':
    autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
    autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
    autoMethod.Refinement = 0  # No refinement
    if nb_elem:
        autoMethod.DefinedBy = PatchIndependentDefineType.ApproxNumElements
        autoMethod.ApproximativeNumberOfElementsPerPart = nb_elem
    elif size_elem:
        autoMethod.DefinedBy = PatchIndependentDefineType.MaxElementSize
        autoMethod.MaximumElementSize = Quantity(size_elem, "mm")
    autoMethod.ElementOrder = ElementOrder.Quadratic
elif type_elem == 'QV':
    autoMethod.Method = MethodType.Cartesian  # Cartesian
    autoMethod.SweepESizeType = 0
    autoMethod.SweepElementSize = Quantity(size, "mm")  # Elem size
    autoMethod.SpacingOption = 0
    autoMethod.ProjectionFactor = 0
    autoMethod.ProjectInConstantZPlane = False
    autoMethod.StretchFactorX = 1
    autoMethod.StretchFactorY = 1
    autoMethod.StretchFactorZ = 1
    autoMethod.CoordinateSystem = model.CoordinateSystems.Children[0]
    autoMethod.WriteICEMCFDFiles = False

# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf


# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path


# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_script_createMesh_QT_nb_elem = \
r"""mesh_save_path = r"{mesh_save_path}"
nb_elem = {nb_elem}

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection

# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
autoMethod.Refinement = 0  # No refinement
autoMethod.DefinedBy = PatchIndependentDefineType.ApproxNumElements
autoMethod.ApproximativeNumberOfElementsPerPart = nb_elem
autoMethod.ElementOrder = ElementOrder.Quadratic
    
# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf

# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path

# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_script_createMesh_LT_nb_elem = \
r"""mesh_save_path = r"{mesh_save_path}"
nb_elem = {nb_elem}

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection

# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
autoMethod.Refinement = 0  # No refinement
autoMethod.DefinedBy = PatchIndependentDefineType.ApproxNumElements
autoMethod.ApproximativeNumberOfElementsPerPart = nb_elem
autoMethod.ElementOrder = ElementOrder.Linear

# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf

# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path

# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_script_createMesh_QT_size_elem = \
r"""mesh_save_path = r"{mesh_save_path}"
size_elem = {size_elem}

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection

# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
autoMethod.Refinement = 0  # No refinement
autoMethod.DefinedBy = PatchIndependentDefineType.MaxElementSize
autoMethod.MaximumElementSize = Quantity(size_elem, "mm")
autoMethod.ElementOrder = ElementOrder.Quadratic

# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf

# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path

# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_script_createMesh_LT_size_elem = \
r"""mesh_save_path = r"{mesh_save_path}"
size_elem = {size_elem}

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection

# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
autoMethod.Refinement = 0  # No refinement
autoMethod.DefinedBy = PatchIndependentDefineType.MaxElementSize
autoMethod.MaximumElementSize = Quantity(size_elem, "mm")
autoMethod.ElementOrder = ElementOrder.Linear

# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf

# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path

# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_script_createMesh_default = \
r"""mesh_save_path = r"{mesh_save_path}"
nb_elem = {nb_elem} * 1000
size_elem = {size_elem}  # Approximate size of elements in mm (may be None if nb_elem is not None)
type_elem = "{type_elem}"  # Type of element. Either 'tet', 'hex' or 'voxel'.

# BUILDING FEA MODEL

# Suppress small bodies
max_volume = max([body.Volume for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body)])
for body in DataModel.GetObjectsByType(Ansys.ACT.Automation.Mechanical.Body):
    if body.Volume == max_volume:
        body.Suppressed = False
    else:
        body.Suppressed = True

#   Get Project's model
model = ExtAPI.DataModel.Project.Model


# Get the whole geometry named selection
geom_ns = model.AddNamedSelection()
geom_ns.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoBody
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns.Generate()  # Generates the named selection

geom_ns_surf = model.AddNamedSelection()
geom_ns_surf.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = geom_ns_surf.GenerationCriteria
criterium = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()  # Criterium to place in the criteria list
criterium.Action = SelectionActionType.Add
criterium.EntityType = SelectionType.GeoFace
criterium.Criterion = SelectionCriterionType.Size
criterium.Operator = SelectionOperatorType.GreaterThan
criterium.Value = Quantity("0 [mm mm]")
GenerationCriteria.Add(criterium)  # Adds criterium to criteria list
geom_ns_surf.Generate()  # Generates the named selection


# Create the Meshing method
autoMethod = model.Mesh.AddAutomaticMethod()
autoMethod.Location = geom_ns

if type_elem == 'QT':
    autoMethod.Method = MethodType.AllTriAllTet  # Tetrahedron
    autoMethod.Algorithm = MeshMethodAlgorithm.PatchIndependent
    autoMethod.Refinement = 0  # No refinement
    if nb_elem:
        autoMethod.DefinedBy = PatchIndependentDefineType.ApproxNumElements
        autoMethod.ApproximativeNumberOfElementsPerPart = nb_elem
    elif size_elem:
        autoMethod.DefinedBy = PatchIndependentDefineType.MaxElementSize
        autoMethod.MaximumElementSize = Quantity(size_elem, "mm")
    autoMethod.ElementOrder = ElementOrder.Quadratic
elif type_elem == 'QV':
    autoMethod.Method = MethodType.Cartesian  # Cartesian
    autoMethod.SweepESizeType = 0
    autoMethod.SweepElementSize = Quantity(size, "mm")  # Elem size
    autoMethod.SpacingOption = 0
    autoMethod.ProjectionFactor = 0
    autoMethod.ProjectInConstantZPlane = False
    autoMethod.StretchFactorX = 1
    autoMethod.StretchFactorY = 1
    autoMethod.StretchFactorZ = 1
    autoMethod.CoordinateSystem = model.CoordinateSystems.Children[0]
    autoMethod.WriteICEMCFDFiles = False

# Creating a boundary condition to avoid error issues
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = geom_ns_surf


# Create the export command
analysis = model.Analyses[0]
cmd = analysis.AddCommandSnippet()
if mesh_save_path.endswith(".cdb"):
    mesh_save_path = mesh_save_path[:-4]
cmd.Input = "cdwrite, db, '%s', cdb" % mesh_save_path


# Solve/Export CDB
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)"""

act_template_get_volume = \
r'''
#### Paths ####
volume_path = r'{volume_path}'

#### Values ####
model = ExtAPI.DataModel.Project.Model

# FIXED #
fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[1]
fixed.XComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.YComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.ZComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
# DISPLACED #
displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[2]
displacement.XComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.YComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(0.001) + ' [mm]')]

### PREPARE OUTPUT ###
#volume_init
volume = model.Analyses[0].Solution.AddVolume()
volume.DisplayOption = ResultAveragingType.ElementalMean

### SOLUTION FOR IMPOSED DISPLACEMENT ###
displacement.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution
#volume_export
volume.ExportToTextFile(True, volume_path)
'''

act_template_get_properties = \
r'''
#### Paths ####
volume_path = r'{volume_path}'

#### Values ####
model = ExtAPI.DataModel.Project.Model

# FIXED #
fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[1]
fixed.XComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.YComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.ZComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
# DISPLACED #
displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[2]
displacement.XComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.YComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(0.001) + ' [mm]')]

### PREPARE OUTPUT ###
#volume_init
#jacobian_init

### SOLUTION FOR IMPOSED DISPLACEMENT ###
displacement.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution
#volume_export
volume.ExportToTextFile(True, volume_path)
'''

act_template_linear = \
r'''#### IDs ####
project_folder = 'D:\Data_L3'
results_folder = 'D:\Data_L3\linear_model_sensitivity'
ID_patient = '{sample}'
resolution = '984mic'
param = '{param}'
location = 'VB'
element_type = '{element_type}'
mat_soft = 'qctma'
material = '{material_law}'

#### Paths ####
mekamesh_path = project_folder + '\\' + ID_patient + '\\' + ID_patient + '_' + resolution + '\\Mesh\\' + ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + param + '_' + mat_soft + '_' + material + '.cdb'
mesh_path = project_folder + '\\' + ID_patient + '\\' + ID_patient + '_' + resolution + '\\Mesh\\' + ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + param + '.cdb'

#### Values ####
model = ExtAPI.DataModel.Project.Model

### Import Named selections ###
model.NamedSelections.InternalObject.ImportNamedSelectionFromCDBFile(mesh_path)
Tree.Refresh()

### LIMIT CONDITIONS ###
# FIXED #
fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[0]
fixed.XComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.YComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.ZComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
# DISPLACED #
displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[1]
displacement.XComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.YComponent.Output.DiscreteValues = [Quantity(str(0.0) + ' [mm]')]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(- 1) + ' [mm]')]

### PREPARE OUTPUT ###
stress = model.Analyses[0].Solution.AddEquivalentStress()
stress.DisplayOption = ResultAveragingType.ElementalMean
elastic_strain = model.Analyses[0].Solution.AddEquivalentElasticStrain()
elastic_strain.DisplayOption = ResultAveragingType.ElementalMean
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
volume = model.Analyses[0].Solution.AddVolume()
volume.DisplayOption = ResultAveragingType.ElementalMean

### SOLUTION FOR IMPOSED DISPLACEMENT ###
displacement.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution
force_reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)
ID_mekamesh = ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + param + '_' + mat_soft + '_' + material
string_results_disp = ID_mekamesh + '\t'
string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
f_reaction = open(results_folder + '\\reaction_force.txt', 'a')
f_reaction.write(string_results_disp)
f_reaction.close()
stress.ExportToTextFile(True, results_folder +'\\' + ID_mekamesh + '_equivalent_stress.txt')
elastic_strain.ExportToTextFile(True, results_folder +'\\' + ID_mekamesh + '_equivalent_elastic_strain.txt')
volume.ExportToTextFile(True, results_folder + '\\' + ID_mekamesh + '_volume.txt')

'''

act_template_EPP = \
r'''#### IDs ####
result_reaction_file=r"{result_reaction_file}"
volume_path = r'{volume_path}'
stress_path = r'{stress_path}'
strain_path = r'{strain_path}'
disp = {disp}
is_EL = {is_EL}

#### Values ####
model = ExtAPI.DataModel.Project.Model

### LIMIT CONDITIONS ###
# FIXED #
fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[1]
fixed.XComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.YComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.ZComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
# DISPLACED #
displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[2]
displacement.XComponent.Output.DiscreteValues = [Quantity(str(disp[0]) + ' [mm]')]
displacement.YComponent.Output.DiscreteValues = [Quantity(str(disp[1]) + ' [mm]')]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp[2]) + ' [mm]')]

### PREPARE OUTPUT ###
stress = model.Analyses[0].Solution.AddEquivalentStress()
stress.DisplayOption = ResultAveragingType.ElementalMean
elastic_strain = model.Analyses[0].Solution.AddEquivalentElasticStrain()
elastic_strain.DisplayOption = ResultAveragingType.ElementalMean
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
volume = model.Analyses[0].Solution.AddVolume()
volume.DisplayOption = ResultAveragingType.ElementalMean

### SOLUTION FOR IMPOSED DISPLACEMENT ###
displacement.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
solution = model.Analyses[0].Solution
force_reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)
ID_mekamesh = "{ID_mekamesh}"
string_results_disp = solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
string_results_disp += 'dt=' + str(solution.ElapsedTime) + 's\t'
string_results_disp += ID_mekamesh + '\t'
string_results_disp += str(disp) + 'mm' + '\t'
string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
f_reaction = open(result_reaction_file, 'a')
f_reaction.write(string_results_disp)
f_reaction.close()
if is_EL:
    stress.ExportToTextFile(True, stress_path)
    elastic_strain.ExportToTextFile(True, strain_path)
    volume.ExportToTextFile(True, volume_path)


'''

act_template_EPP_remote_point = \
r'''#### IDs ####
result_reaction_file=r"{result_reaction_file}"
results_folder=r"{results_folder}"
disp_list = {disp_list}
RPX, RPY, RPZ = {remote_point}
all_times = {all_times}
top_index = {top_index}
bottom_index = {bottom_index}


#### Values ####
model = ExtAPI.DataModel.Project.Model

### LIMIT CONDITIONS ###
# FIXED #
fixed = model.Analyses[0].AddFixedSupport()
fixed.Location = model.NamedSelections.Children[bottom_index]

# REMOTE POINT #
remote_points_1 = Model.RemotePoints
remote_point_1 = remote_points_1.AddRemotePoint()
remote_point_1.ScopingMethod = GeometryDefineByType.Component
remote_point_1.Location = model.NamedSelections.Children[top_index]
remote_point_1.Behavior = LoadBehavior.Rigid
remote_point_1.XCoordinate = Quantity(RPX, "mm")
remote_point_1.YCoordinate = Quantity(RPY, "mm")
remote_point_1.ZCoordinate = Quantity(RPZ, "mm")

# REMOTE DISPLACEMENT #
displacement = model.Analyses[0].AddRemoteDisplacement()
displacement.Location = model.RemotePoints.Children[0]

### PREPARE OUTPUT ###
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
elastic_strain = model.Analyses[0].Solution.AddEquivalentElasticStrain()
elastic_strain.DisplayOption = ResultAveragingType.ElementalMean
plastic_strain = model.Analyses[0].Solution.AddEquivalentPlasticStrain()
plastic_strain.DisplayOption = ResultAveragingType.ElementalMean
volume = model.Analyses[0].Solution.AddVolume()
volume.DisplayOption = ResultAveragingType.ElementalMean

for disp in disp_list:
    try:
        displacement.XComponent.Output.DiscreteValues = [Quantity(str(disp[0]) + ' [mm]')]
        displacement.YComponent.Output.DiscreteValues = [Quantity(str(disp[1]) + ' [mm]')]
        displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp[2]) + ' [mm]')]
    
        ### SOLUTION FOR IMPOSED DISPLACEMENT ###
        displacement.Suppressed = False
        ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
        solution = model.Analyses[0].Solution
        if solution.Status == SolutionStatusType.Done:
            force_reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)
            ID_mekamesh = "{ID_mekamesh}"
            if all_times:
                # read time steps
                path_time = solution.WorkingDir + 'file.aapresults'
                f_time = open(path_time, 'r')
                lines = f_time.readlines()
                step_times = []
                for line in lines:
                    if line.find("e-") != -1 or line.find("e+") != -1:
                        step_times.append(float(line))
                f_time.close()
                string_results_disp = ""
                for time in step_times:
                    reaction.DisplayTime = Quantity(time, "s")
                    plastic_strain.DisplayTime = Quantity(time, "s")
                    ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
                    string_results_disp += solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
                    string_results_disp += 'dt=' + str(solution.ElapsedTime) + 's\t'
                    string_results_disp += ID_mekamesh + '\t'
                    string_results_disp += str(disp) + 'mm' + '\t'
                    string_results_disp += str(time) + 's' + '\t'
                    string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
                    string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
                    string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
                    string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
                    plastic_strain.ExportToTextFile(True, results_folder +'\\' + ID_mekamesh + '_' + str(time) + '_equivalent_plastic_strain.txt')
                volume.ExportToTextFile(True, results_folder + '\\' + ID_mekamesh + '_volume.txt')
            else:
                string_results_disp = solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
                string_results_disp += 'dt=' + str(solution.ElapsedTime) + 's\t'
                string_results_disp += ID_mekamesh + '\t'
                string_results_disp += str(disp) + 'mm' + '\t'
                string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
                elastic_strain.ExportToTextFile(True, results_folder +'\\' + ID_mekamesh + '_equivalent_elastic_strain.txt')
                volume.ExportToTextFile(True, results_folder + '\\' + ID_mekamesh + '_volume.txt')
        else:
            string_results_disp = solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
            string_results_disp += ID_mekamesh + '\t'
            string_results_disp += str(disp) + 'mm' + '\t'
            string_results_disp += '########FAIL#########' + '\t'
            string_results_disp += 'dt=' + str(solution.Status) + '\n'
    except error as e:
        string_results_disp = '########FAIL######### ' + str(e) + '\n'
    f_reaction = open(result_reaction_file, 'a')
    f_reaction.write(string_results_disp)
    f_reaction.close()
    

'''



act_template_EPP_all_times = \
r'''#### IDs ####
result_reaction_file=r"{result_reaction_file}"
results_folder=r"{results_folder}"
disp = {disp}
all_times = True

#### Values ####
model = ExtAPI.DataModel.Project.Model

### LIMIT CONDITIONS ###
# FIXED #
fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[1]
fixed.XComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.YComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
fixed.ZComponent.Output.DiscreteValues = [Quantity('0 [mm]')]
# DISPLACED #
displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[2]
displacement.XComponent.Output.DiscreteValues = [Quantity(str(disp[0]) + ' [mm]')]
displacement.YComponent.Output.DiscreteValues = [Quantity(str(disp[1]) + ' [mm]')]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp[2]) + ' [mm]')]

### PREPARE OUTPUT ###
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
plastic_strain = model.Analyses[0].Solution.AddEquivalentPlasticStrain()
plastic_strain.DisplayOption = ResultAveragingType.ElementalMean
volume = model.Analyses[0].Solution.AddVolume()
volume.DisplayOption = ResultAveragingType.ElementalMean

try:
    displacement.XComponent.Output.DiscreteValues = [Quantity(str(disp[0]) + ' [mm]')]
    displacement.YComponent.Output.DiscreteValues = [Quantity(str(disp[1]) + ' [mm]')]
    displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp[2]) + ' [mm]')]

    ### SOLUTION FOR IMPOSED DISPLACEMENT ###
    displacement.Suppressed = False
    ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
    solution = model.Analyses[0].Solution
    if solution.Status == SolutionStatusType.Done:
        force_reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)
        ID_mekamesh = "{ID_mekamesh}"
        if all_times:
            # read time steps
            path_time = solution.WorkingDir + 'file.aapresults'
            f_time = open(path_time, 'r')
            lines = f_time.readlines()
            step_times = []
            for line in lines:
                if line.find("e-") != -1 or line.find("e+") != -1:
                    if step_times != []:
                        step_times.append((float(line) - step_times[-1])/2 + step_times[-1])
                    step_times.append(float(line))
            f_time.close()
            string_results_disp = ""
            for time in step_times:
                reaction.DisplayTime = Quantity(time, "s")
                plastic_strain.DisplayTime = Quantity(time, "s")
                ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
                string_results_disp += solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
                string_results_disp += 'dt=' + str(solution.ElapsedTime) + 's\t'
                string_results_disp += ID_mekamesh + '\t'
                string_results_disp += str(disp) + 'mm' + '\t'
                string_results_disp += str(time) + 's' + '\t'
                string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
                string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
                plastic_strain.ExportToTextFile(True, results_folder +'\\' + ID_mekamesh + '_' + str(time) + '_equivalent_plastic_strain.txt')
            volume.ExportToTextFile(True, results_folder + '\\' + ID_mekamesh + '_volume.txt')
        else:
            string_results_disp = solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
            string_results_disp += 'dt=' + str(solution.ElapsedTime) + 's\t'
            string_results_disp += ID_mekamesh + '\t'
            string_results_disp += str(disp) + 'mm' + '\t'
            string_results_disp += str(force_reaction[0].XAxis).split('[')[0] + '\t'
            string_results_disp += str(force_reaction[0].YAxis).split('[')[0] + '\t'
            string_results_disp += str(force_reaction[0].ZAxis).split('[')[0] + '\t'
            string_results_disp += str(force_reaction[0].Total).split('[')[0] + '\t\n'
    else:
        string_results_disp = solution.DateOfRun + '-' + solution.TimeOfRun + '\t'
        string_results_disp += ID_mekamesh + '\t'
        string_results_disp += str(disp) + 'mm' + '\t'
        string_results_disp += '########FAIL#########' + '\t'
        string_results_disp += 'dt=' + str(solution.Status) + '\n'
except error as e:
    string_results_disp = '########FAIL######### ' + str(e) + '\n'
f_reaction = open(result_reaction_file, 'a')
f_reaction.write(string_results_disp)
f_reaction.close()


'''