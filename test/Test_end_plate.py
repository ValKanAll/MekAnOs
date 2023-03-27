from Geometry_modifyer.SetNamedSelections import read_pstf_vertebra, detect_endplate

pstf_path = r"H:\Lyos_JPR_data_2011_vertebrae_L3_no_default_with_endplate\17_2007\17_2007_984mic\17_2007_984mic_VB_EF.pstf"
read_pstf_vertebra(pstf_path, 1)
stl_path = r"H:\Lyos_JPR_data_2011_vertebrae_L3_no_default_with_endplate\17_2007\17_2007_984mic\17_2007_984mic_VB_EF.stl"
#detect_endplate(stl_path, sample=4000, distance=0.2, plot=2, endplate_height=4.5)