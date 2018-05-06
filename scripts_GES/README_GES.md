# AVEC_2018
Baseline scripts of the 8th Audio/Visual Emotion Challenge.

#REQUIREMENT
These are the following library you need to install to use these scripts :
	- Numpy (sudo apt-get python-numpy on Ubuntu)
	- Scipy (sudo apt-get python-scipy on Ubuntu)
	- Matplotlib (sudo apt-get python-matplotib on Ubuntu)
	- Liblinear (2.20) : don't forget to set up the config file with base folder for python
	- Liac-arff (2.1.1) (sudo python -m pip install --user liac-arff on Ubuntu)

#HOW TO SET UP
First of all you must set all the variables in the Config/Config.py file.
Please be sure to put a / at the end of each folder.
The base folders will be those in the AVEC2018, please don't change structure or name, otherwise it won't work.

#HOW TO RUN
For the Gold Standard Creation (recreating in the GS Folder the baseline Gold Standard), go in the GoldStandardCreation
folder and type "python GSCreationMain.py"
For the Audio Prediction, go in the AudioPred folder and type "python AudioPredMain.py", if you don't put any argument the multimodal prediction will launch
Otherwise you can put a number for the modality (for the number correspondance, type "python AudioPredMain.py help")
And for the Test Prediction, go in the TestPred folder and type "python TestPredMain.py"

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN WINDOWS (7/64bits for me)
- First of all you need to download python2.7, you can get it here : https://www.python.org/downloads/release/python-2715/
  Take the "Windows x86-64 MSI installer"
- After you have installed it, you need to add environment variables, there is a tutorial here : https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
  You should set one var called PYTHON_HOME to c:\Python27 (or the path you have installed python) and the other var called path, you must add %PYTHON_HOME%;%PYTHON_HOME%\Scripts\;
- After you need pip to install others libraries, download it from here : https://bootstrap.pypa.io/get-pip.py
- When this is done open a CMD in administrator mode and go the directory where you have downloaded it (cd PATH)
- Then run "python get-pip.py", this will install it (This should have added environment variables for pip but if you can't lauch it from everywhere you need to add these
- After you need to install numpy/scipy/matplotlib/liac-arff : just type "python -m pip install --user numpy scipy matplotlib liac-arff" on cmd
- Now you need to install liblinear (you can install it with pip but this is not the last version) : http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Just unzip liblinear, put it somewhere and put the address to the python folder within
- And it's good, you just need now to set up the project

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN LINUX (Ubuntu 16.04 for me)
- First of all you need to install python2.7 : "sudo apt-get install python"
- You need to install pip : "sudo apt-get install pip"
- For installing the library type : "python -m pip install --user numpy scipy matplotlib liac-arff"
- Now you need to install liblinear (you can install it with pip but this is not the last version) : http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Just unzip liblinear, put it somewhere and put the address to the python folder within
- And it's good, you just need now to set up the project

#HOW TO INSTALL PYTHON AND ALL LIBRARY IN MACOS
#TODO
