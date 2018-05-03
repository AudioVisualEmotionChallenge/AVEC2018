# AVEC_2018
Baseline scripts of the 8th Audio/Visual Emotion Challenge.

#REQUIREMENT
These are the following library you need to install to use these scripts :
	- Numpy (sudo apt-get python-numpy on Ubuntu)
	- Scipy (sudo apt-get python-scipy on Ubuntu)
	- Matplotlib (sudo apt-get python-matplotib on Ubuntu)
	- Liblinear (2.20) : don't forget to set up the config file with base folder
	- Liac-arff (2.1.1) : should be compiled to be imported
	- OpenSmile (2.3.0) : don't forget to set up the config file with base folder

#HOW TO SET UP
First of all you must set all the variables in the Config/Config.py file.
Please be sure to put a / at the end of each folder.
The base folders will be used with differents subfolders like "Norm"/"Conc", prefer using empty one.

#HOW TO RUN
For the Audio Extraction (using eGeMAPSv01a), go in the AudioExtract folder and type "python AudioExtract.py"
For the Gold Standard Creation (recreating in the GS Folder the baseline Gold Standard), go in the GoldStandardCreation
folder and type "python GSCreation.py"
For the Audio Prediction, go in the AudioPred folder and type "python AudioPred.py"
And for the Test Prediction, go in the TestPred folder and type "python TestPred.py"
