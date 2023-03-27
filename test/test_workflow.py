from Workflow.FEA_model import FEA_model

''' WORKFLOW
This script creates a finite element model of vertebral body using the segmentation 
all the way to the estimation of bone strength.
'''
# Define steps you want to process, if False, only parameters are given but step ss not processed
detect_endplates = False
create_mesh = False
inject_materials = False
attribute_law = True
add_endplates = True
simulate = True

'''
First, define a model by choosing the dataset name, sample name and segmentation
Information is gathered in Data/Samples.xlsx
'''
# Parameters to define model
dataset_name = 'Lokbani et al. (2022)'  # Source et al. (year)
sample = '01_2005'
segmentation = 'L1_def_VB_transformed'# Resolution_number+mic_VB_initials operator
# Model definition
model = FEA_model(dataset_name, sample, segmentation)

'''
Second, detect the endplates and generate a position file (.pstf) with its own axis and endplates threshold.
If plot = 1, you can watch the results
'''

model.detect_endplates(plot=1, check=False)

'''
Third, segmentation is converted to a mesh without mechanical properties (yet)
Depending on the element type, the parameters will be interpreted differently
1st letter corresponds to element order: linear (L), or quadratic (Q)
2nd letter corresponds to element shape: tetrahedron (T), hexahedron (H), voxel (V)
3rd letter corresponds to the method of creation:
    - Element volume (V): only for tetrahedron and means the parameter will define the mean value of each element 
    volume in mm^3. Using the total volume of the vertebral body divided by the element volume we compute a number 
    of elements as an input for Ansys.
    - Number of elements (N): only for tetrahedron
    - Element size (S): element's characteristic length
    - Number of divisions(D): only for hexahedron and voxel. Meshing is done along the Z-axis with the defined number 
    of divisions. The resulting spacing is reported on X and Y if their factor is equal to 1.
Param: 
For V: volume of element in mm^3
For N: Number of element desired
For S: Characteristic dimension of the element in mm
For D:  Defined a slice number in 
Example: QTV - Quadratic Tetrahedron defined by element volume in mm^3
'''
# Parameters for meshing

element_type = 'QTV'
param = 1

# Meshing command
model.create_mesh(element_type, param, check=False)


'''
Fourth, the affectation of density to each element by positioning the mesh into the scan.
Using QCTMA, each element is attributed a mean density weighed by the proportion of volume of each voxel inside the 
element. Densities are then converted to Young's modulus using the density to E relationship in the given config. Materials
are limited using the delta_E value. Materials are gathered in delta_E steps.
For example if delta_E equals 10 MPa, there will be a material each 10 MPa.
This is due to Ansys not being able to handle a high number of materials. min_E is the minimum value affected for the 
materials. A value too low might create issues with weak elements highly distorted.
Finally, each material is affected properties described in the given config
'''
# Parameters for material attribution
delta_E = 10
min_E = 1
config = 'KopEPP07'

# Material attribution
model.inject_materials(delta_E, min_E, config=config, check=False)

'''
Fifth, add boundary conditions selection, especially endplates here.
Endplates are added from .pstf file
'''
model.add_endplates(process=True)

'''
Sixth, simulate
'''
result_path = r"H:\Data_WL\01_2005.txt"  # add path-result\filename.txt
model.simulate(result_path, process=simulate)

