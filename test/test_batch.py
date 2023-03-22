from Workflow.Batch import Batch

'''
In this script you can run several parameters to study their influence.
It also makes easier the launching of multiple simulations at once.
'''

# define parameters
dataset = 'Wegrzyn et al. (2011)'
segmentation_list = ['984mic_VB']
mesh_param_list = [['QTV', 1]]  # [element_type, param]
qctma_param_list = [[10, 0.1], [10, 0.01], [10, 0.001]]  # [material_step, min_E]
config_list = ['KopEPP07']
simulation_model = 'Lyon'
check = True  # if True, it will check if files were created before creating them

# create batch
b = Batch(dataset, segmentation_list, mesh_param_list, qctma_param_list, config_list, simulation_model, check)

# launch batch
b.process()