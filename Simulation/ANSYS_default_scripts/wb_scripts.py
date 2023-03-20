wb_script_createMesh_default = \
r"""# encoding: utf-8
# 2019 R1
SetScriptVersion(Version="19.3.111")

STL_PATH = r"{stl_path}"
SCRIPT_PATH = r"{act_script_path}"
    
unitSystem1 = SetProjectUnitSystem(UnitSystemName="NMM_STANDARD")

template = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
system = template.CreateSystem()
geometryComp = system.GetContainer(ComponentName="Geometry")
geometryComp.SetFile(FilePath=STL_PATH)

modelComponent = system.GetComponent(Name="Model")
modelComponent.Refresh()

Simulation.RunScript(FilePath=SCRIPT_PATH, IsMeshing=False, ModelName="Model")

"""

wb_script_simulation_default = \
r"""
# encoding: utf-8
# 2019 R1
SetScriptVersion(Version="19.3.111")
Reset()
project_folder = 'D:\Data_L3'
results_folder = 'D:\Data_L3\linear_model_sensitivity'
ID_patient = '{sample}'
resolution = '984mic'
param = '{param}'
location = 'VB'
element_type = '{element_type}'
mat_soft = 'qctma'
material_law = '{material_law}'
path_act = r'{path_act}'


path_logfile = r"{path_logfile}"
logfile = open(path_logfile, 'a')
logfile.write(ID_patient + '\t' + param + '\t' + material_law + '\n')
print('start')

path_act = r"{path_act}"
mekamesh_path = project_folder + '\\' + ID_patient + '\\' + ID_patient + '_' + resolution + '\\Mesh\\' + ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + param + '_' + mat_soft + '_' + material_law + '.cdb'
print(mekamesh_path)
template1 = GetTemplate(TemplateName="External Model")
system1 = template1.CreateSystem()
setup1 = system1.GetContainer(ComponentName="Setup")
externalModelFileData1 = setup1.AddDataFile(FilePath=mekamesh_path)
template2 = GetTemplate(
    TemplateName="Static Structural",
    Solver="ANSYS")
system2 = template2.CreateSystem(
    Position="Right",
    RelativeTo=system1)
setupComponent1 = system1.GetComponent(Name="Setup")
engineeringDataComponent1 = system2.GetComponent(Name="Engineering Data")
setupComponent1.TransferData(TargetComponent=engineeringDataComponent1)
modelComponent1 = system2.GetComponent(Name="Model")
setupComponent1.TransferData(TargetComponent=modelComponent1)
model1 = system2.GetContainer(ComponentName="Model")
meshConversionOptions1 = model1.GetMeshConversionOptions()  
meshConversionOptions1.CreateGeometry = False
logfile.write('model file open\n')
try:
    print('update')
    Update()
    logfile.write('model updated, ready for simulation\n')
    logfile.write('simulation running\n')
    Simulation.RunScript(FilePath=path_act, IsMeshing=False, ModelName='Model')
    logfile.write('simulation done\n')

except error:
    logfile.write(error)
    logfile.write('\n')
    logfile.write('error during update\n')
#model1.Edit()
logfile.close()
"""

wb_script_simulation_EPP = r"""
# encoding: utf-8
# 2021 R1
path_act=r"{path_act}" 
mekamesh_path=r"{mekamesh_path}"
SetScriptVersion(Version="21.1.216")
template1 = GetTemplate(TemplateName="External Model")
system1 = template1.CreateSystem()
template2 = GetTemplate(
    TemplateName="Static Structural",
    Solver="ANSYS")
system2 = template2.CreateSystem(
    Position="Right",
    RelativeTo=system1)
setupComponent1 = system1.GetComponent(Name="Setup")
engineeringDataComponent1 = system2.GetComponent(Name="Engineering Data")
setupComponent1.TransferData(TargetComponent=engineeringDataComponent1)
modelComponent1 = system2.GetComponent(Name="Model")
setupComponent1.TransferData(TargetComponent=modelComponent1)
setup1 = system1.GetContainer(ComponentName="Setup")
externalModelFileData1 = setup1.AddDataFile(FilePath=mekamesh_path)
externalModelFileDataProperty1 = externalModelFileData1.GetDataProperty()
externalModelFileDataProperty1.CheckValidBlockedCdbFile = False
model1 = system2.GetContainer(ComponentName="Model")
meshConversionOptions1 = model1.GetMeshConversionOptions()
meshConversionOptions1.CreateGeometry = False
setupComponent2 = system2.GetComponent(Name="Setup")
setupComponent2.UpdateUpstreamComponents()
Simulation.RunScript(FilePath=path_act, IsMeshing=False, ModelName='Model')
"""