from Batch.FEA_model import FEA_model

''' WORKFLOW
This script creates a finite element model of vertebral body using the segmentation 
all the way to the estimation of bone strength.
'''
# Define steps you want to process, if False, only parameters are given but step ss not processed
detect_endplates = False
create_mesh = False
inject_materials = False
attribute_law = True

'''
First, define a model by choosing the dataset name, sample name and segmentation
Information is gathered in Data/Samples.xlsx
'''
# Parameters to define model
dataset_name = 'Wegrzyn et al. (2011)'  # Source et al. (year)
sample = '01_2007'
segmentation = '328mic_VB_EF'  # Resolution_number+mic_VB_initials operator #TODO put it clearer on excel
# Model definition
model = FEA_model(dataset_name, sample, segmentation)

'''
Second, detect the endplates and generate a position file (.pstf) with its own axis and endplates threshold.
If plot = 1, you can watch the results
'''
model.detect_endplates(plot=1, process=detect_endplates)

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
element_type = 'LTN'
param = 10000

# Meshing command
model.create_mesh(element_type, param, process=create_mesh)


'''
Fourth, the affectation of density to each element by positioning the mesh into the scan.
Using QCTMA, each element is attributed a mean density weighed by the proportion of volume of each voxel inside the 
element. Densities are then converted to Young's modulus using Kopperdahl et al. (2002) linear relationship. Materials
are limited using the delta_E value. Materials are gathered in delta_E steps.
For example if delta_E equals 10 MPa, there will be a material each 10 MPa.
This is due to Ansys not being able to handle a high number of materials. min_E is the minimum value affected for the 
materials. A value too low might create issues with weak elements highly distorted.
'''
# Parameters for material attribution
delta_E = 20
min_E = 1

# Material attribution
model.inject_materials(delta_E, min_E, process=inject_materials)

'''
Fifth, attribution of constitutive law
Each config has a name and can be found in Data/Literature_laws.mkbl
'''
config = 'KopEPP10'
model.set_constitutive_laws(config, process=attribute_law)

'''
Sixth, add boundary conditions selection, especially endplates here.
Endplates are added from .pstf file
'''
model.add_endplates()

'''
Seventh, simulate
'''
result_path=r"E:\Data_L3\test_result_17_03_23.txt"  # add path-result\filename.txt
model.simulate(result_path)