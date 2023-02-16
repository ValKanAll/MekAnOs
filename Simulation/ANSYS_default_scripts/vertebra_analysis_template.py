
### Infos
sample = {sample}
element_type = {element_type}
nb_elements = {nb_elements}
material_step = {material_step}
material_law = {material_law}
coef_poisson = {coef_poisson}
disp_value = {disp_value}

### Paths
path_results_folder = r'{path_results_folder}'
path_act_script = r"{path_act_script}"
path_named_selections = r"{path_named_selections}"
path_log_file = r"{path_logfile}"

model = ExtAPI.DataModel.Project.Model

# Change working directory

logfile = open(path_log_file, 'a')
logfile.write('0 - Starting simulation - {} {} {} {} {} {}\n'.format(sample, element_type, nb_elements, material_step, material_law, coef_poisson))

# Import Named selections
try:
    model.NamedSelections.InternalObject.ImportNamedSelectionFromCDBFile(path_named_selections)
    Tree.Refresh()
    logfile.write('1 - Named selections imported\n')
except:
    logfile.write('X - Error with named selection importation\n')

# Create conditions

fixed = model.Analyses[0].AddNodalDisplacement()
fixed.Location = model.NamedSelections.Children[0]
fixed.XComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
fixed.YComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
fixed.ZComponent.Output.DiscreteValues = [Quantity("0 [mm]")]

displacement = model.Analyses[0].AddNodalDisplacement()
displacement.Location = model.NamedSelections.Children[1]
displacement.XComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
displacement.YComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
displacement.ZComponent.Output.DiscreteValues = [Quantity(str(disp_value) + " [mm]")]

logfile.write('2 - Boundary conditions imposed\n')

# Prepare output

stress = model.Analyses[0].Solution.AddEquivalentStress()
strain = model.Analyses[0].Solution.AddEquivalentElasticStrain()
reaction = model.Analyses[0].Solution.AddForceReaction()
reaction.BoundaryConditionSelection = fixed
volume = model.Analyses[0].Solution.AddVolume()

# Solution imposed displacement

displacement.Suppressed = False
ExtAPI.DataModel.Project.Model.Analyses[0].Solution.Solve(True)
logfile.write('3 - Simulation starting\n')
solution = model.Analyses[0].Solution
logfile.write('4 - Simulation solved\n')

elastic_stress = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StressResults.EquivalentStress, solution.Children)
elastic_strain = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.StrainResults.EquivalentElasticStrain, solution.Children)
reaction = filter(lambda item: item.GetType() == Ansys.ACT.Automation.Mechanical.Results.ProbeResults.ForceReaction, solution.Children)

string_data = '{}\t{}\t{}\t{}\t{}\t{}\t'.format(sample, element_type, nb_elements, material_step, material_law, coef_poisson)
string_results_disp = str(reaction[0].XAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].YAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].ZAxis).split('[')[0]+'\t'
string_results_disp += str(reaction[0].Total).split('[')[0]+'\t'

# Export Results

f = open(path_results_folder + '\\results.txt', 'a')
f.write(string_data + '\\' + string_results_disp + '\n')
f.close()

elastic_stress.ExportToTextFile(True, path_results_folder + '\\{}_{}_elastic_stress.txt'.format(sample, material_step+'v'+coef_poisson))
elastic_strain.ExportToTextFile(True, path_results_folder + '\\elastic_strain.txt')
volume.ExportToTextFile(True, path_results_folder + '\\volume.txt')

logfile.write('5 - Results exported')
logfile.close()
"""



