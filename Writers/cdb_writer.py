

def int_printer(integer, int_format):
    len_int = len(str(integer))
    if len_int > int_format:
        raise NameError('format for integer {} is not high enough'.format(integer))
    else:
        return ' '*(int_format - len_int) + str(integer)


def float_printer(float, float_format):
    # scientific writing of float
    sci_float = '%.{}E'.format(float_format[1]) % float
    len_float = len(sci_float)
    if len_float > float_format[0]:
        raise NameError('format for float is not high enough')
    else:
        return ' '*(float_format[0] - len_float) + sci_float


def write_node_line(node, int_format, float_format):
    #print('node ', node.get_ID_node())
    output = int_printer(node.get_ID_node(), int_format) + int_printer(0, int_format) + int_printer(0, int_format)
    output += float_printer(node.get_x(), float_format)
    output += float_printer(node.get_y(), float_format)
    output += float_printer(node.get_z(), float_format)
    output += '\n'
    return output


def write_element_line(element, int_format, is_mekamesh=True):
    node_list = element.get_node_list()
    index = 0
    if is_mekamesh:
        output = int_printer(element.get_ID_material(), int_format) + '\n' * (1 if index == 18 else 0)
        index = ((index + 1) if index < 18 else 0)
    else:
        output = int_printer(1, int_format) + '\n' * (1 if index == 18 else 0)
        index = ((index + 1) if index < 18 else 0)
    output += int_printer(element.get_ID_element_type(), int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(1, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(1, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(0, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(0, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(0, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(0, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(len(node_list), int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(0, int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    output += int_printer(element.get_ID(), int_format) + '\n' * (1 if index == 18 else 0)
    index = ((index + 1) if index < 18 else 0)
    #print('element ', element.get_ID_element())
    for node_ID in node_list:
        output += int_printer(node_ID, int_format) + '\n' * (1 if index == 18 else 0)
        index = ((index + 1) if index < 18 else 0)
    output += '\n'
    return output


def write_node_block(file, node_list, int_format=7, float_format=(22, 13)):
    print('WRITE NODE BLOCK')
    num_node = len(node_list)
    part = num_node // 10
    file.write('NBLOCK,6,SOLID,'+ int_printer(num_node, int_format) + ',' + int_printer(num_node, int_format) + '\n')
    file.write('(3i{},6e{}.{})\n'.format(int_format, float_format[0], float_format[1]))
    index = 0
    for node in node_list:
        file.write(write_node_line(node, int_format, float_format))
        index += 1
        if index % part == 0:
            k = index // part
            print('{}% '.format(10*k)+k*'-'+(10-k)*' ')
    file.write('N,R5.3,LOC,' + int_printer(-1, int_format) + ',\n\n')


def write_element_block(file, element_list, int_format=10, is_mekamesh=True):
    print('WRITE ELEMENT BLOCK')
    num_element = len(element_list)
    part = num_element // 10
    file.write('EBLOCK,19,SOLID,' + int_printer(num_element, int_format) + ',')
    file.write(int_printer(num_element, int_format) + '\n')
    file.write('(19i{})\n'.format(int_format))
    index = 0
    for element in element_list:
        file.write(write_element_line(element, int_format, is_mekamesh))
        index += 1
        if index % part == 0:
            k = index // part
            print('{}% '.format(10 * k) + k * '-' + (10 - k) * ' ')
    file.write(int_printer(-1, int_format) + '\n')


def write_element_type_block(file, element_type_list):
    for element_type in element_type_list:
        if element_type[1] == 'quadratic tetrahedron':
            element_type_ref = '187'
        elif element_type[1] == 'linear hexahedron':
            element_type_ref = '185'
        elif element_type[1] == 'quadratic hexahedron':
            element_type_ref = '186'
        elif element_type[1] == 'linear tetrahedron':
            element_type_ref = '285'
        file.write('ET,{},{}\n'.format(str(element_type[0]), element_type_ref))
    file.write('\n')


def write_prop(prop, value, material_ID):
    if value:
        output = 'MPTEMP,R5.0, 1, 1,  0.00000000    ,\n' #MPTEMP defines temperature table
        output += 'MPDATA,R5.0, 1,{},     {}, 1,{}    ,\n'.format(prop, material_ID, str(value))
    else:
        output = ''
    return output


def write_prop_plastic(yield_strength, plastic_modulus, material_ID):
    if yield_strength:
        output = 'TB,BISO,       {},   1\n'.format(material_ID)
        output += 'TBTEM,  0.00000000    ,   1\n'
        output += 'TBDAT,      1,{}    , {},\n'.format(str(yield_strength), str(plastic_modulus))
    else:
        #print('Problem with material {}, PM={}, YS={}'.format(material_ID, plastic_modulus, yield_strength))
        output = ''
    return output


def write_material_block(file, material_list):
    for material in material_list:
        material_ID = material.get_ID()
        file.write(write_prop('EX', material.get_EX(), material_ID))
        file.write(write_prop('EY', material.get_EY(), material_ID))
        file.write(write_prop('EZ', material.get_EZ(), material_ID))

        file.write(write_prop('DENS', material.get_DENS(), material_ID))

        file.write(write_prop('NUXY', material.get_NUXY(), material_ID))
        file.write(write_prop('NUYZ', material.get_NUYZ(), material_ID))
        file.write(write_prop('NUXZ', material.get_NUXZ(), material_ID))

        file.write(write_prop('GXY', material.get_GXY(), material_ID))
        file.write(write_prop('GYZ', material.get_GYZ(), material_ID))
        file.write(write_prop('GXZ', material.get_GXZ(), material_ID))

        file.write(write_prop_plastic(material.get_yield_strength(), material.get_plastic_modulus(), material_ID))


def write_cdb_file(path, mesh):
    if type(mesh).__name__ == 'Mekamesh':
        is_mekamesh = True
    elif type(mesh).__name__ == 'Mesh':
        is_mekamesh = False

    file = open(path, 'w')
    file.write('/PREP7\n')
    write_node_block(file, mesh.get_node_list())
    write_named_selections_block(file, mesh.get_named_selections_list())
    write_element_type_block(file, mesh.get_element_type_list())
    write_element_block(file, mesh.get_element_list(), 7, is_mekamesh)
    if is_mekamesh:
        write_material_block(file, mesh.get_material_list())
    file.write('\n/GO\nFINISH\n')

    file.close()


def write_named_selections_block(file, named_selections_list, int_format=10):
    for named_selections in named_selections_list:
        file.write('CMBLOCK,{},NODE,{}\n'.format(named_selections[0], int_printer(len(named_selections[1]), 8)))
        file.write('(8i{})\n'.format(int_format))
        index = 1
        for node in named_selections[1]:
            file.write(int_printer(node, int_format))
            if index%8 == 0:
                file.write('\n')
            index += 1
        file.write('\n\n')


def write_named_selections(path, named_selections_list, int_format=10):
    file = open(path, 'w')
    for named_selections in named_selections_list:
        file.write('CMBLOCK,{},NODE,{}\n'.format(named_selections[0], int_printer(len(named_selections[1]), 8)))
        file.write('(8i{})\n'.format(int_format))
        index = 1
        for node in named_selections[1]:
            file.write(int_printer(node, int_format))
            if index%8 == 0:
                file.write('\n')
            index += 1
        file.write('\n')
    file.close()
    return path


