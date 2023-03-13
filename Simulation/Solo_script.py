import datetime
import subprocess

"""Purpose of this script is to launch any workbench script"""

wb_script_path = r"E:\Data_IBHGC\WB_scripts\448_L3_VB_QT_2_wb_script.py"

_cmd = r'"C:\Program Files\ANSYS Inc\v211\Framework\bin\Win64\RunWB2.exe"  -B -R "%s"' % wb_script_path
try:
    print("\tCMD: ", _cmd)
    t0 = datetime.datetime.now()
    print("\tStarted at: ", t0)
    subprocess.check_call(_cmd, shell=True)
    t1 = datetime.datetime.now()
    print("\tDuration: ", t1 - t0)
except subprocess.CalledProcessError as error:
    print(error)