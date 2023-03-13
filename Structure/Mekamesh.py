from Reader.cdb_reader import read_cdbfile
from Writer.cdb_writer import write_cdb_file
from Structure.Mesh import Mesh


class Mekamesh(Mesh):
    def __init__(self, path, parent=None):
        Mesh.__init__(self, path, parent)
    # TODO delete number_element

    # Define dependencies
        self.is_loaded = False
        self.material_list = []
        self.element_list = []
        self.node_list = []
        self.named_selections_list = []
        self.loaded_lonely_faces = False
        self.mechanical_law_list = []
        self.density_step = None
        self.material_step = None
        self.HU_step = None

    def set_material_step(self, value):
        self.material_step = value

    def get_material_step(self):
        return self.material_step

    def set_density_step(self, new_density_step):
        self.density_step = new_density_step

    def get_density_step(self):
        return self.density_step

    def set_mechanical_law_list(self, mechanical_law_list):
        self.mechanical_law_list = mechanical_law_list

    def get_mechanical_law_list(self):
        return self.mechanical_law_list

    def set_material_list(self, new_material_list):
        self.material_list = new_material_list

    def get_infos(self):
        infos = [['Description', True, [['Object', 'Mechanical mesh'], ['Path', self.path], ['Number of elements', str(self.number_element)]]],
                ['Element types', True, [[str(element_type[0]), element_type[1], str(element_type[2])] for element_type in self.element_type_list],
                ['Named selections', True, [[named_selections[0], str(len(named_selections[1])) + ' nodes'] for named_selections in self.named_selections_list]]]]
        material_info = []
        for material in self.material_list:
            material_info.append([str(material.get_ID()), True, material.get_properties()])
        infos.append(['Materials', False, material_info])
        return infos

    def get_attributes_infos(self):
        self.attribute_list = [['Mekamesh', self.path.split('/')[-1]]]
        self.attribute_list += [['Named selections', named_selections[0]] for named_selections in self.named_selections_list]
        return self.attribute_list

    def get_attributes(self):
        self.attribute_list = [self]
        self.attribute_list += self.named_selections_list
        return self.attribute_list

    def get_attributes_property(self):
        '''return a list of mesh properties (elements, materials)'''
        if not self.is_loaded:
            self.read()
        return [['Elements', self.element_list],
                ['Materials', self.material_list]
                ]

    def get_material_list(self):
        if self.is_loaded:
            return self.material_list
        else:
            self.read()
            return self.material_list

    def read(self):
        if not self.is_loaded:
            if self.path:
                read_cdbfile(self.path, self)
                #self.get_nodes_dict()
                self.get_element_dict()
                #self.get_lonely_faces_nodes()
                self.is_loaded = True
            else:
                raise NameError('missing path for mekamesh')

    def unread(self):
        # empty memory of elements and nodes
        self.is_loaded = False
        self.element_list = []
        self.node_list = []
        self.material_list = []

        self.named_selections_list = []
        try:
            del self.element_dict
            del self.nodes_dict
        except AttributeError:
            pass

        self.loaded_lonely_faces = False
        self.lonely_faces_nodes = []

    def write(self, new_path=None):
        if self.is_loaded:
            if new_path:
                self.path = new_path
            write_cdb_file(self.path, self)
        else:
            raise NameError('File is not loaded so cannot be written')


if __name__ == '__main__':
    import datetime


    def volume_plastic_euler(ID_patient, nb_elements, mat_soft, material):
        t0 = datetime.datetime.now()
        folder = "/Users/valentinallard/Desktop/Doctorat/Simulation/linear_model/"
        project_folder = 'D:\Data_L3'
        results_folder = 'D:\Data_L3\linear_model_sensitivity'
        mesh_path = project_folder + '\\' + ID_patient + '\\' + ID_patient + '_' + resolution + '\\Mesh\\' + ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + str(nb_elements) + 'k' + '.cdb'
        mekamesh = Mekamesh('', mesh_path)
        mekamesh.read()
        t1 = datetime.datetime.now()
        print('time to read : {}'.format(t1-t0))
        ID_mekamesh = ID_patient + '_' + resolution + '_' + location + '_' + element_type + '_' + str(
            nb_elements) + 'k' + '_' + mat_soft + '_' + material

        volume_path = results_folder + '\\' + ID_mekamesh + '_volume.txt'
        strain_path = results_folder + '\\' + ID_mekamesh + '_equivalent_elastic_strain.txt'

        volume_plastic = 0
        disp_1 = 1
        volume_1 = mekamesh.get_contiguous_plastic_volume(0.015, strain_path, volume_path, disp_1)
        disp_0 = 0.1
        volume_0 = mekamesh.get_contiguous_plastic_volume(0.015, strain_path, volume_path, disp_0)
        volume_2_egalize = 0.000001

        plastic_loop_count = 0
        while abs(volume_plastic - volume_2_egalize)/volume_2_egalize > 0.05 and plastic_loop_count < 100:
            f_prime = (volume_1 - volume_0)/(disp_1 - disp_0)
            disp = disp_1 - (volume_1 - volume_2_egalize)/f_prime
            volume_plastic = mekamesh.get_contiguous_plastic_volume(0.015, strain_path, volume_path, disp)
            print('*** disp = {}/// volume_plastic = {}'.format(disp, volume_plastic))
            if volume_0 < volume_plastic < volume_1:
                disp_1 = disp
                volume_1 = volume_plastic
            elif volume_plastic < volume_0:
                disp_1 = disp_0
                volume_1 = volume_0
                disp_0 = disp
                volume_0 = volume_plastic
            elif volume_plastic > volume_1:
                disp_0 = disp_1
                volume_0 = volume_1
                disp_1 = disp
                volume_1 = volume_plastic
            print('plastic_loop_count = {}'.format(plastic_loop_count))
            plastic_loop_count += 1
            if abs(disp_0 - disp_1) < 10 ^ (-10):
                return disp_0

        print('final_disp', disp)
        return(disp)

    def volume_plastic_dicot(mesh_path, results_folder, ID_mekamesh, elastic_strain_threshold=0.015, volume_2_egalize=1000, error=0.05):
        """
        Gets contiguouss plastic volume for linear simulation
        :param mesh_path:
        :param results_folder:
        :param ID_mekamesh:
        :param elastic_strain_threshold:
        :param volume_2_egalize:
        :param error:
        :return: returns displacement to match given contiguous plastic_volume in mm
        """
        t0 = datetime.datetime.now()
        mekamesh = Mekamesh('', mesh_path)
        mekamesh.read()
        t1 = datetime.datetime.now()
        print('time to read : {}'.format(t1-t0))
        volume_path = results_folder + '\\' + ID_mekamesh + '_volume.txt'
        strain_path = results_folder + '\\' + ID_mekamesh + '_equivalent_elastic_strain.txt'

        volume_plastic = 0
        disp_1 = 1
        volume_1 = mekamesh.get_contiguous_plastic_volume(elastic_strain_threshold, strain_path, volume_path, disp_1)
        disp_0 = 0.5
        volume_0 = mekamesh.get_contiguous_plastic_volume(elastic_strain_threshold, strain_path, volume_path, disp_0)

        plastic_loop_count = 0
        while abs(volume_plastic - volume_2_egalize)/volume_2_egalize > error and plastic_loop_count < 100:
            while volume_1 < volume_2_egalize:
                disp_1 = 1.5*disp_1
                volume_1 = mekamesh.get_contiguous_plastic_volume(elastic_strain_threshold, strain_path, volume_path, disp_1)
            while volume_2_egalize < volume_0:
                disp_0 = 0.5 * disp_0
                volume_0 = mekamesh.get_contiguous_plastic_volume(elastic_strain_threshold, strain_path, volume_path, disp_0)
            disp = (disp_0 + disp_1) / 2
            volume_plastic = mekamesh.get_contiguous_plastic_volume(elastic_strain_threshold, strain_path, volume_path, disp)
            print('*** disp = {}/// volume_plastic = {}'.format(disp, volume_plastic))
            if volume_plastic <= volume_2_egalize:
                disp_0 = disp
                volume_0 = volume_plastic
            elif volume_2_egalize <= volume_plastic:
                disp_1 = disp
                volume_1 = volume_plastic
            print('plastic_loop_count = {}'.format(plastic_loop_count))
            plastic_loop_count += 1
            if abs(disp_0 - disp_1) < 10 ^ (-10):
                return disp_0

        print('final_disp', disp)
        return(disp, volume_plastic)

    def contiguous_volume_plastic(mesh_path, results_folder, ID_mekamesh, strain_threshold=0.015, disp=1):
        t0 = datetime.datetime.now()
        mekamesh = Mekamesh('', mesh_path)
        mekamesh.read()
        t1 = datetime.datetime.now()
        print('time to read : {}'.format(t1-t0))

        volume_path = results_folder + '\\' + ID_mekamesh + '_volume.txt'
        strain_path = results_folder + '\\' + ID_mekamesh + '_equivalent_elastic_strain.txt'

        return mekamesh.get_contiguous_plastic_volume(strain_threshold, strain_path, volume_path, disp)

    displacements = []
    sample_list = [#'01_2007', '02_2007', '07_2007', '08_2007', '11_2007', '12_2007', '13_2007',
        #'15_2007', '16_2007',
        #'17_2007', '18_2007', '19_2007',
        #           '20_2007', '03', '31', '32'
        #'35', '37', '40', '43', '44'
        '2a_2005_L1',
        '2b_2005_L1',
        '03_2006_L1',
        '04_2006_L1',
        '05_2006_L1',
        '06_2006_L1',
        '08_2006_L1',
        '10_2006_L1',
        'USOD18433_L1',
        'USOD20307_L1'
    ]
    element_type_list = ['QV']
    material_law_list = [# '1v03', '1v04',
                         #'2v03', '2v04', '5v03', '5v04', '10v03',
        '10v03']#, '20v03', '20v04', '50v03', '50v04']
    param_list = ['1mm']
    location = 'VB'
    resolution = 'def'
    mat_software = 'qctma'
    results_analysis = r"D:\Data_post-defect_2021-05-18\linear_model_sensitivity\analysis_volume.txt"
    #with open(results_analysis) as f:
    #    line = f.readline()

    for patient in sample_list:
        for element_type in element_type_list:
            for material_law in material_law_list:
                for param in param_list:
                    print('************ {} {} {} {} ************'.format(patient, element_type, material_law, param))
                    try:
                        displacements.append([patient, param, mat_software, material_law,
                                              volume_plastic_dicot(patient, param, mat_software, material_law)])
                    except FileNotFoundError as e:
                        print(e)
                    '''print(line)
                    disp = float(line.split('/')[4].split('\n')[0])
                    displacements.append([patient, nb_element, mat_software, material_law, disp, contiguous_volume_plastic(patient, nb_element, mat_software, material_law, disp)])
                    line = f.readline()'''
    for d in displacements:
        print(d)


