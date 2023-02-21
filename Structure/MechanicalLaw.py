class MechanicalLaw:
    def __init__(self, law_name, law_property, a, b, c, min_value=0.001, site='', source='', densitometric_measure='', unit=''):
        self.law_name = law_name
        self.law_property = law_property
        self.site = site # anatomical site
        self.source = source
        self.densitometric_measure = densitometric_measure
        self.unit = unit
        # property = a + b*density**c
        self.a = a
        self.b = b
        self.c = c
        self.min_value = min_value

    def __str__(self):
        return('[name={}, prop={}, a={}, b={}, c={}, min={}]'.format(self.law_name, self.law_property, self.a, self.b, self.c, self.min_value))

    def get_law_name(self):
        return self.law_name

    def get_law_property(self):
        return self.law_property

    def get_site(self):
        return self.site

    def get_source(self):
        return self.source

    def get_densitometric_measure(self):
        return self.densitometric_measure

    def get_equation(self):
        a = self.a
        b = self.b
        c = self.c
        min = self.min_value

        def equation(density):
            return max(a + b*density**c, min)

        return equation

    def get_coefficients(self):
        return self.a, self.b, self.c

    def set_law_property(self, new_prop):
        self.law_property = new_prop
        return self.law_property

    def set_law_name(self, new_law_name):
        self.law_name = new_law_name
        return self.law_name

    def set_site(self, new_site):
        self.site = new_site
        return self.site

    def set_source(self, new_source):
        self.source = new_source
        return self.source

    def set_densitometric_measure(self, new_densitometric_measure):
        self.densitometric_measure = new_densitometric_measure
        return self.densitometric_measure

    def set_equation(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        return self.a, self.b, self.c


EX_Keller1994SpinePower = MechanicalLaw('Keller1994SpinePower', 'EX', 0, 1890, 1.92, 0.001, 'spine', 'Keller (1994)', 'rho_ash', 'MPa')
EX_Keaveny1997LumbarLinear = MechanicalLaw('Keaveny1997LumbarLinear', 'EX', -58, 1540, 1, 0.001, 'lumbar spine', 'Keaveny et al. (1997)', 'rho_app', 'MPa')
EX_KopperdahlKeaveny1998SpineLinear = MechanicalLaw('KopperdahlKeaveny1998SpineLinear', 'EX', -80, 2100, 1, 0.001, 'spine', 'Kopperdahl and Keaveny (1998)', 'rho_app', 'MPa')
EX_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'EX', -34.7, 3230, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EX_Kopperdahl2002SpineLinearTransverse = MechanicalLaw('Kopperdahl2002SpineLinearTransverse', 'EX', -34.7/3, 3230/3, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EX_Morgan2003SpinePower = MechanicalLaw('Morgan2003SpinePower', 'EX', 0, 4730, 1.56, 0.001, 'spine', 'Morgan et al. (2003)', 'rho_app', 'MPa')

EY_Keller1994SpinePower = MechanicalLaw('Keller1994SpinePower', 'EY', 0, 1890, 1.92, 0.001, 'spine', 'Keller (1994)', 'rho_ash', 'MPa')
EY_Keaveny1997LumbarLinear = MechanicalLaw('Keaveny1997LumbarLinear', 'EY', -58, 1540, 1, 0.001, 'lumbar spine', 'Keaveny et al. (1997)', 'rho_app', 'MPa')
EY_KopperdahlKeaveny1998SpineLinear = MechanicalLaw('KopperdahlKeaveny1998SpineLinear', 'EY', -80, 2100, 1, 0.001, 'spine', 'Kopperdahl and Keaveny (1998)', 'rho_app', 'MPa')
EY_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'EY', -34.7, 3230, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EY_Kopperdahl2002SpineLinearTransverse = MechanicalLaw('Kopperdahl2002SpineLinearTransverse', 'EY', -34.7/3, 3230/3, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EY_Morgan2003SpinePower = MechanicalLaw('Morgan2003SpinePower', 'EY', 0, 4730, 1.56, 0.001, 'spine', 'Morgan et al. (2003)', 'rho_app', 'MPa')

EZ_Keller1994SpinePower = MechanicalLaw('Keller1994SpinePower', 'EZ', 0, 1890, 1.92, 0.001, 'spine', 'Keller (1994)', 'rho_ash', 'MPa')
EZ_Keaveny1997LumbarLinear = MechanicalLaw('Keaveny1997LumbarLinear', 'EZ', -58, 1540, 1, 0.001, 'lumbar spine', 'Keaveny et al. (1997)', 'rho_app', 'MPa')
EZ_KopperdahlKeaveny1998SpineLinear = MechanicalLaw('KopperdahlKeaveny1998SpineLinear', 'EZ', -80, 2100, 1, 0.001, 'spine', 'Kopperdahl and Keaveny (1998)', 'rho_app', 'MPa')
EZ_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'EZ', -34.7, 3230, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EZ_Kopperdahl2002SpineLinearTransverse = MechanicalLaw('Kopperdahl2002SpineLinearTransverse', 'EZ', -34.7/3, 3230/3, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
EZ_Morgan2003SpinePower = MechanicalLaw('Morgan2003SpinePower', 'EZ', 0, 4730, 1.56, 0.001, 'spine', 'Morgan et al. (2003)', 'rho_app', 'MPa')

GXY_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'GXY', -34.7*0.121, 3230*0.121, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')

GXZ_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'GXZ', -34.7*0.157, 3230*0.157, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')

GYZ_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'GYZ', -34.7*0.157, 3230*0.157, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')

NUXY_03 = MechanicalLaw('NU03', 'NUXY', 0.3,  0, 0)
NUXY_033 = MechanicalLaw('NU033', 'NUXY', 0.33,  0, 0)
NUXY_011 = MechanicalLaw('NU011', 'NUXY', 0.11,  0, 0)

NUYZ_03 = MechanicalLaw('NU03', 'NUYZ', 0.3,  0, 0)
NUYZ_033 = MechanicalLaw('NU033', 'NUYZ', 0.33,  0, 0)
NUYZ_011 = MechanicalLaw('NU011', 'NUYZ', 0.11,  0, 0)

NUXZ_03 = MechanicalLaw('NU03', 'NUXZ', 0.3,  0, 0)
NUXZ_033 = MechanicalLaw('NU033', 'NUXZ', 0.33,  0, 0)
NUXZ_011 = MechanicalLaw('NU011', 'NUXZ', 0.11,  0, 0)


YS_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'yield_strength', -0.750, 24.9, 1, 0.001, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')


PM_Perfect_Plasticity_0kPa = MechanicalLaw('PerfectPlasticity', 'plastic_modulus', 0, 0, 1, 0, '', '', '', 'MPa')
PM_Perfect_Plasticity_1MPa = MechanicalLaw('PerfectPlasticity1MPa', 'plastic_modulus', 1, 0, 1, 0.001, '', '', '', 'MPa')
PM_Perfect_Plasticity_200kPa = MechanicalLaw('PerfectPlasticity200kPa', 'plastic_modulus', 0.2, 0, 1, 0.001, '', '', '', 'MPa')
PM_Perfect_Plasticity_1kPa = MechanicalLaw('PerfectPlasticity1kPa', 'plastic_modulus', 0.001, 0, 1, 0.001, '', '', '', 'MPa')
PM_Perfect_Plasticity_1Pa = MechanicalLaw('PerfectPlasticity1Pa', 'plastic_modulus', 0.000001, 0, 1, 0.001, '', '', '', 'MPa')

global_list_EX = [EX_Keller1994SpinePower,
                  EX_Keaveny1997LumbarLinear,
                  EX_KopperdahlKeaveny1998SpineLinear,
                  EX_Kopperdahl2002SpineLinear,
                  EX_Kopperdahl2002SpineLinearTransverse,
                  EX_Morgan2003SpinePower
                  ]

global_list_EY = [EY_Keller1994SpinePower,
                  EY_Keaveny1997LumbarLinear,
                  EY_KopperdahlKeaveny1998SpineLinear,
                  EY_Kopperdahl2002SpineLinear,
                  EY_Kopperdahl2002SpineLinearTransverse,
                  EY_Morgan2003SpinePower
                  ]

global_list_EZ = [EZ_Keller1994SpinePower,
                  EZ_Keaveny1997LumbarLinear,
                  EZ_KopperdahlKeaveny1998SpineLinear,
                  EZ_Kopperdahl2002SpineLinear,
                  EZ_Kopperdahl2002SpineLinearTransverse,
                  EZ_Morgan2003SpinePower
                  ]

global_list_NUXY = [NUXY_03, NUXY_033, NUXY_011]
global_list_NUYZ = [NUYZ_03, NUYZ_033, NUYZ_011]
global_list_NUXZ = [NUXZ_03, NUXZ_033, NUXZ_011]

global_list_GXY = [GXY_Kopperdahl2002SpineLinear]
global_list_GYZ = [GYZ_Kopperdahl2002SpineLinear]
global_list_GXZ = [GXZ_Kopperdahl2002SpineLinear]

global_list_YS = [YS_Kopperdahl2002SpineLinear
                  ]
global_list_PM = [
                  PM_Perfect_Plasticity_0kPa,
                  PM_Perfect_Plasticity_1MPa,
                  PM_Perfect_Plasticity_200kPa,
                  PM_Perfect_Plasticity_1kPa,
                  PM_Perfect_Plasticity_1Pa
                  ]