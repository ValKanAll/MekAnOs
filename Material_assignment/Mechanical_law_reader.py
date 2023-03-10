from Structure.MechanicalLaw import MechanicalLaw


global_list_EX = []
global_list_EY = []
global_list_EZ = []
global_list_GXY = []
global_list_GYZ = []
global_list_GXZ = []
global_list_NUXY = []
global_list_NUYZ = []
global_list_NUXZ = []
global_list_YS = []
global_list_PM = []


def read_mkbl_file(path):
    global global_list_EX, global_list_EY, global_list_EZ
    global global_list_GXY, global_list_GYZ, global_list_GXZ
    global global_list_NUXY, global_list_NUYZ, global_list_NUXZ
    global global_list_YS
    global global_list_PM
    """
    Extract mechanical laws from datafile.
    :param path: Path to the file.
    :return: list of mechanical law.
    """
    with open(path, 'r', errors="ignore") as f:
        line = f.readline()
        while line:
            # print(line)
            # suppress comments
            if line.find('#') != -1:
                line = line[:line.find('#')]
            if line in ['', '\n']:
                line = f.readline()
                continue
            is_version = line.find('! version = ')
            if is_version != -1:
                version = line[:is_version]
                line = f.readline()
                continue
            # DETECTING TABLE OF COORDINATE (NODES)
            else:
                law_line = line.split('\n')[0].split(' ')
                if int(law_line[0]) == 1:
                    source = law_line[1]
                    year = law_line[2]
                    location = law_line[3]
                    law_type = law_line[4]
                    a = float(law_line[6])
                    b = float(law_line[7])
                    c = float(law_line[8])
                    min_value = float(law_line[9])
                    measure = law_line[10]
                    unit = law_line[11]
                    name = source + year + location + law_type
                    prop = law_line[5]

                elif int(law_line[0]) == 2:
                    name = law_line[1]
                    source = ''
                    year = ''
                    location = ''
                    prop = law_line[2]
                    a = float(law_line[3])
                    b = float(law_line[4])
                    c = float(law_line[5])
                    min_value = 0
                    measure = ''
                    unit = ''

                elif int(law_line[0]) == 3:
                    name = law_line[1]
                    source = ''
                    year = ''
                    location = ''
                    prop = law_line[2]
                    a = float(law_line[3])
                    b = float(law_line[4])
                    c = float(law_line[5])
                    min_value = float(law_line[6])
                    measure = ''
                    unit = law_line[7]

                elif int(law_line[0]) == 4:
                    name = law_line[1]
                    prop = law_line[2]
                    eps_y = float(law_line[3])
                    global_list_YS += [MechanicalLaw(name, 'YS', 0, eps_y, 1, 0.001, '',
                                                     '', 'EX', 'MPa')]



                if prop == 'E':
                    global_list_EX += [MechanicalLaw(name, 'EX', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_EY += [MechanicalLaw(name, 'EY', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_EZ += [MechanicalLaw(name, 'EZ', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]

                elif prop == 'G':
                    global_list_GXY += [MechanicalLaw(name, 'GXY', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_GYZ += [MechanicalLaw(name, 'GYZ', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_GXZ += [MechanicalLaw(name, 'GXZ', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]

                elif prop == 'NU':
                    global_list_NUXY += [MechanicalLaw(name, 'NUXY', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_NUYZ += [MechanicalLaw(name, 'NUYZ', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]
                    global_list_NUXZ += [MechanicalLaw(name, 'NUXZ', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]

                elif prop == 'YS' and int(law_line[0]) == 1:
                    global_list_YS += [MechanicalLaw(name, 'YS', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]

                elif prop == 'PM':
                    global_list_PM += [MechanicalLaw(name, 'PM', a, b, c, min_value, location,
                                                    source + '(' + year + ')', measure, unit)]

                line = f.readline()
                continue
    f.close()

import os
print(os.getcwd())
try:
    read_mkbl_file('../Data/Litterature_laws.mkbl')
except FileNotFoundError:
    read_mkbl_file('../../Data/Litterature_laws.mkbl')



