#!/bin/python2
# python2 script
# Extract acoustic features for all audio files of the AVEC 2018 Cross-cultural Emotion Sub-Challenge (CES)
# Put the scripts into a subfolder of the AVEC2018_CES package, e.g., AVEC2018_CES/scripts/
# Output: csv files

import os
import time

# MODIFY HERE
folder_data   = '../audio/'           # folder with audio (.wav) files
folder_output = '../audio_features/'  # output folder
exe_opensmile = '/tools/opensmile-2.3.0/bin/linux_x64_standalone_static/SMILExtract'  # MODIFY this path to the folder of the SMILExtract (version 2.3) executable
path_config   = '/tools/opensmile-2.3.0/config/'                                      # MODIFY this path to the config folder of opensmile 2.3 - no POSIX here on cygwin (windows)

conf_smileconf = path_config + 'MFCC12_0_D_A.conf'  # MFCCs 0-12 with delta and acceleration coefficients

opensmile_options = '-configfile ' + conf_smileconf + ' -appendcsv 0 -timestampcsv 1 -headercsv 1'  # options from standard_data_output_lldonly.conf.inc

if not os.path.exists(folder_output):
    os.mkdir(folder_output)

for fn in os.listdir(folder_data):
    infilename  = folder_data + fn
    instname    = os.path.splitext(fn)[0]
    outfilename = folder_output + instname + '.csv'
    opensmile_call = exe_opensmile + ' ' + opensmile_options + ' -inputfile ' + infilename + ' -csvoutput ' + outfilename + ' -instname ' + instname + ' -output ?'  # (disabling htk output)
    os.system(opensmile_call)
    time.sleep(0.01)

os.remove('smile.log')

