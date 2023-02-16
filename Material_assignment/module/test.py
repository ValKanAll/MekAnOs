from module.Converters.ModifyMechanicalLaw import create_new_mekamesh_from_mekamesh
from module.Structure.Mekamesh import Mekamesh
from module.Structure.MechanicalLaw import MechanicalLaw



L = ['01_2007', '07_2007', '11_2007', '12_2007', '13_2007', '15_2007', '16_2007', '17_2007', '19_2007',
     '03', '31', '32', '35', '37', '40', '43', '44']

NUXY_03 = MechanicalLaw('NU03', 'NUXY', 0.3,  0, 0)
EX_Keller1998SpinePower = MechanicalLaw('Keller1994SpinePower', 'EX', 0, 1890, 1.92, 0.01, 'spine', 'Keller (1994)', 'rho_ash', 'MPa')
YS_Kopperdahl2002SpineLinear = MechanicalLaw('Kopperdahl2002SpineLinear', 'YS', -0.750, 24.9, 1, 0.01, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
YS_Keller1998SpineLinear = MechanicalLaw('Keller1998SpineLinear', 'YS', 0, 1890*0.007, 1.92, 0.01, 'spine', 'Kopperdahl et al. (2002)', 'rho_app', 'MPa')
PM_Perfect_Plasticity_0kPa = MechanicalLaw('PerfectPlasticity', 'PM', 0, 0, 1, 0, '', '', '', 'MPa')
EX_Prado3_2020SpinePower = MechanicalLaw('Prado3_2020SpinePower', 'EX', 0, 10494, 1.56, 0.01, 'spine', 'Prado (2020)', 'rho_ash', 'MPa')
YS_Prado3_2020SpinePower = MechanicalLaw('Prado3_2020SpinePower', 'YS', 0, 10494*0.007, 1.56, 0.01, 'spine', 'Prado et al. (2020)', 'rho_app', 'MPa')
EX_Morgan2003SpinePower = MechanicalLaw('Morgan2003SpinePower', 'EX', 0, 4730, 1.56, 0.001, 'spine', 'Morgan et al. (2003)', 'rho_app', 'MPa')
YS_Morgan2003SpinePower = MechanicalLaw('Morgan2003SpinePower', 'YS', 0, 4730*0.007, 1.56, 0.01, 'spine', 'Morgan et al. (2003)', 'rho_app', 'MPa')

for patient in L:
    path = '/Users/valentinallard/Downloads/Data_L3_987mic_VB_QT_1mm_bonemat_1MPa/' + patient + '_984mic_VB_QT_1mm_bonemat_1MPa.cdb'
    ID = path.split('/')[-1]
    mekamesh = Mekamesh(ID, path)
    mekamesh.read()
    '''
    # Keller EL
    config_meca = 'Keller1998-EL-iso'
    mechanical_law_list = [EX_Keller1998SpinePower, NUXY_03]
    material_step_type = ''
    value_step = 10
    approximation = 'mid'

    create_new_mekamesh_from_mekamesh(mekamesh, config_meca, mechanical_law_list, material_step_type, value_step, approximation)

    # Keller EPP
    config_meca = 'Keller1998-EPP-iso'
    mechanical_law_list = [EX_Keller1998SpinePower, NUXY_03, YS_Keller1998SpineLinear, PM_Perfect_Plasticity_0kPa]
    material_step_type = ''
    value_step = 10
    approximation = 'mid'

    create_new_mekamesh_from_mekamesh(mekamesh, config_meca, mechanical_law_list, material_step_type, value_step,
                                      approximation)
    '''
    # Prado EPP
    config_meca = 'Prado2020-EPP-iso'
    mechanical_law_list = [EX_Prado3_2020SpinePower, NUXY_03, YS_Prado3_2020SpinePower, PM_Perfect_Plasticity_0kPa]
    material_step_type = ''
    value_step = 10
    approximation = 'mid'

    create_new_mekamesh_from_mekamesh(mekamesh, config_meca, mechanical_law_list, material_step_type, value_step,
                                      approximation)
                                      
    '''
    # Morgan EPP
    config_meca = 'Morgan2003-EPP-iso'
    mechanical_law_list = [EX_Morgan2003SpinePower, NUXY_03, YS_Morgan2003SpinePower, PM_Perfect_Plasticity_0kPa]
    material_step_type = ''
    value_step = 10
    approximation = 'mid'

    create_new_mekamesh_from_mekamesh(mekamesh, config_meca, mechanical_law_list, material_step_type, value_step,
                                      approximation)
                                      
    '''
