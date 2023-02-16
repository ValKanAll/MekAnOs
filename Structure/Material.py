class Material:
    def __init__(self, ID_material):
        '''
        EX : Young's modulus along X axis
        EY : Young's modulus along Y axis
        EZ : Young's modulus along Z axis
        NUXY : Poisson's ratio XY
        NUYZ : Poisson's ratio YZ
        NUXZ : Poisson's ratio XZ
        GXY : Shear modulus XY
        GYZ : Shear modulus YZ
        GXZ : Shear modulus XZ
        :param ID_material: material identification, usually a number
        '''
        self.ID_material = ID_material
        self.EX = None
        self.EY = None
        self.EZ = None
        self.NUXY = None
        self.NUYZ = None
        self.NUXZ = None
        self.GXY = None
        self.GYZ = None
        self.GXZ = None
        self.DENS = None
        self.yield_strength = None
        self.plastic_modulus = None

        self.element_occurence = 0

        self.properties_dict = {
               'Density': None,
               'EX': None,
               'EY': None,
               'EZ': None,
               'NUXY': None,
               'NUYZ': None,
               'NUXZ': None,
               'GXY': None,
               'GYZ': None,
               'GXZ': None,
               'DENS': None,
               'yield_strength': None,
               'plastic_modulus': None
                           }

    def clean(self):
        self.properties_dict = {
            'Density': self.DENS,
            'EX': None,
            'EY': None,
            'EZ': None,
            'NUXY': None,
            'NUYZ': None,
            'NUXZ': None,
            'GXY': None,
            'GYZ': None,
            'GXZ': None,
            'DENS': None,
            'yield_strength': None,
            'plastic_modulus': None
        }
        self.EX = None
        self.EY = None
        self.EZ = None
        self.NUXY = None
        self.NUYZ = None
        self.NUXZ = None
        self.GXY = None
        self.GYZ = None
        self.GXZ = None
        self.yield_strength = None
        self.plastic_modulus = None

    def get_properties(self):
        result = [['Element occurence', str(self.element_occurence)]]
        for key_prop in self.properties_dict:
            if self.properties_dict[key_prop]:
                result.append([key_prop, self.properties_dict[key_prop]])
        return result

    def get_ID(self):
        return self.ID_material

    def get_EX(self):
        return self.EX

    def get_EY(self):
        return self.EY

    def get_EZ(self):
        return self.EZ

    def get_DENS(self):
        return self.DENS

    def get_NUXY(self):
        return self.NUXY

    def get_NUYZ(self):
        return self.NUYZ

    def get_NUXZ(self):
        return self.NUXZ

    def get_GXY(self):
        return self.GXY

    def get_GYZ(self):
        return self.GYZ

    def get_GXZ(self):
        return self.GXZ

    def get_yield_strength(self):
        return self.yield_strength

    def get_plastic_modulus(self):
        return self.plastic_modulus

    def set_DENS(self, value, unit='10^9.kg.m^-3'):
        self.DENS = value
        self.properties_dict['Density'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.DENS_unit = unit
        else:
            raise NameError('unit value for DENS is not string type')

    def set_EX(self, value, unit='MPa'):
        self.EX = value
        self.properties_dict['EX'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.EX_unit = unit
        else:
            raise NameError('unit value for EX is not string type')

    def set_EY(self, value, unit='MPa'):
        self.EY = value
        self.properties_dict['EY'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.EY_unit = unit
        else:
            raise NameError('unit value for EY is not string type')

    def set_EZ(self, value, unit='MPa'):
        self.EZ = value
        self.properties_dict['EZ'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.EZ_unit = unit
        else:
            raise NameError('unit value for EZ is not string type')

    def set_NUXY(self, value):
        self.NUXY = value
        self.properties_dict['NUXY'] = str(value)

    def set_NUYZ(self, value):
        self.NUYZ = value
        self.properties_dict['NUYZ'] = str(value)

    def set_NUXZ(self, value):
        self.NUXZ = value
        self.properties_dict['NUXZ'] = str(value)

    def set_GXY(self, value, unit='MPa'):
        self.GXY = value
        self.properties_dict['GXY'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.GXY_unit = unit
        else:
            raise NameError('unit value for GXY is not string type')

    def set_GYZ(self, value, unit='MPa'):
        self.GYZ = value
        self.properties_dict['GYZ'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.GYZ_unit = unit
        else:
            raise NameError('unit value for GYZ is not string type')

    def set_GXZ(self, value, unit='MPa'):
        self.GXZ = value
        self.properties_dict['GXZ'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.GXZ_unit = unit
        else:
            raise NameError('unit value for GXZ is not string type')

    def set_yield_strength(self, value, unit='MPa'):
        self.yield_strength = value
        self.properties_dict['yield_strength'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.yield_strength_unit = unit
        else:
            raise NameError('unit value for yield_strength is not string type')

    def set_plastic_modulus(self, value, unit='MPa'):
        self.plastic_modulus = value
        self.properties_dict['plastic_modulus'] = str(value) + ' ' + unit
        if type(unit) == str:
            self.plastic_modulus_unit = unit
        else:
            raise NameError('unit value for plastic_modulus is not string type')

    def set_element_occurence(self, occurence):
        if type(occurence) == int:
            self.element_occurence = occurence
        else:
            raise NameError('Element occurence of material is not type int')

    def get_element_occurence(self):
        return self.element_occurence

