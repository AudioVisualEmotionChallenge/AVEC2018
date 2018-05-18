# AVEC 2018
Baseline scripts of the AVEC 2018 Gold-Standard Emotion Sub-challenge.

#REQUIREMENT
These are the following library you need to install to use these scripts :
- Numpy
- Scipy
- Matplotlib
- Liblinear (2.20) : don't forget to set up the config file with base folder for python
- Liac-arff (2.1.1)
- Sklearn (0.19.1)

#HOW TO SET UP
First of all you must set all the variables in the Config/Config.py file.
Please be sure to put a / at the end of each folder.
The base folders will be those of the AVEC_2018 GES repository; structure and name of the files must be preserved.

#HOW TO RUN
For Gold Standard Creation (recreating in the GS Folder the baseline Gold Standard) :
- Go in the GoldStandardCreation folder
- Type "python GSCreationMain.py"
- Results will go to "gs_created" folder.
For the Audio Prediction :
- Go in the AudioPred folder
- Type "python PredMain.py ARGS"
- If you don't put any argument the multimodal prediction will launch.
- Otherwise you can put a number for the modality (for the number correspondance, type "python AudioPredMain.py help")

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN WINDOWS (tested on Windows 7 - 64bits)
- Download python2.7, you can get it here : https://www.python.org/downloads/release/python-2715/
- Take the "Windows x86-64 MSI installer"
- After installation, environment variables must be set, there is a tutorial here : https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
  You should set "PYTHON_HOME" to "c:\Python27" (or the path you have installed python) and to var "path", you must add "%PYTHON_HOME%;%PYTHON_HOME%\Scripts\;"
- Install pip, download link here : https://bootstrap.pypa.io/get-pip.py
- Open a CMD in administrator mode
- Go to the folder where get-pip.py is (cd PATH)
- Run "python get-pip.py", this will install it (Environment variables should be set for pip but if you can't lauch it from everywhere you need to add these too)
- Install the libraries : "python -m pip install --user numpy scipy matplotlib liac-arff sklearn" on cmd
- Install liblinear (pip have not the last version) : http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Unzip liblinear and put the address to the python folder within
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN LINUX (tested on Ubuntu 16.04/14.04)
- First install python2.7 : "sudo apt-get install python"
- Install pip : "sudo apt-get install pip"
- Install the libraries : "python -m pip install --user numpy scipy matplotlib liac-arff sklearn"
- Install liblinear (pip have not the last version) : http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Unzip liblinear and put the address to the python folder within
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN MACOS
#TODO
