#Baseline scripts of the AVEC 2018 GES

#GENERAL DESCRIPTION OF THE SYSTEM

The scripts allow to train and optimise a multimodal emotion recognition system on the RECOLA dataset to predict emotion labels (arousal or valence), either provided in the data package, or by the participant, every 400 ms. 
Performance is measured by the concordance correlation coefficient between the gold-standard and the series of predictions (average of the CCC over the recordings) obtained on the development and test partitions. 
Results on the test partition, which will serve for ranking the submissions, cannot be reproduced since test labels are not available, despite we provide the script for full transparency.

#AUDIOVISUAL FEATURES (external access)

The emotion recognition system exploits audio, video and physiological signals, with different representations that are either hand-crafted or learned in an unsupervised way. 

More precisely, audio features include:
- functionals of Low-Level-Descriptors using the eGeMAPS hand-crafted feature set with openSMILE; fixed analysis windows with size ranging from 3 seconds to 9 seconds,
- Bags-of-Audio-Words using openXBOW; codebook size is 100, soft assignment, words computed from 12 MFCCs + log energy, with delta and delta-delta; same window size as used for eGeMAPS,
- unsupervised features using auDeep; a representation of the raw waveform is learned by a deep autoencoder where sparse features are obtained by the activation function of each neuron of the hidden to last layer connection. 

Video features include:
- functionals of appearance and geometric based features (same set as used in the AVEC 2016 MASC Sub-challenfge),
- functionals of Facial Action Units (openFACE; intensity of 17 FAUs),
- Bags-of-Video-Words computed from the FAUs using openXBOW; same configuration as for Bags-of-Audio-Words, and
- all video feautures are extracted with sliding windows and with the same range of duration as used for audio data. 

Physiological features include a set of functionals computed over the ECG, EDA and their related signals (HR, SCL, and SCR); the same set of features of the AVEC 2016 MASC Sub-challenge is used.

#SYSTEM ARCHITECTURE

The architecture of the recognition system is hierarchical and starts with a series of models learned on the training set for each modality and each representation. 
The models include: 
- Support Vector Machines (L2-L2 dual form of the regression solver) from the liblinear library, and  
- Generalised Linear Models (ridge regression, lasso, multi-task lasso, elastic net, and multi-task elastic net) from the scikit machine learning toolbox. 

Optimisation of each model is performed on the development partition by performing a grid-search over the following parameters: 
- window size, 
- time delay uniformly applied to the gold-standard, 
- regularisation coefficients (complexity for SVR, alpha for generalised linear models), and 
- post-processing parameters (bias and scaling factor).

Features of each set (training, development and test) are standardised using the first two statistical moments computed on the training set. Selection of the best model and its corresponding hyper-parameters is done on the development partition. 

Two different late fusion strategies are then compared: 
- One that fuses all predictions obtained by the different modalities (audio, video, and physiogical) and their corresponding representation (functionals, bags-of-words, and unsupervised deep learning), 
- Another that fuses each represantation of the different modalities, and then the obtained series of predictions over the modalities. 
Optimisation of the regression models used for the fusion processes includes only the regularisation parameter alpha. 
Replication of the best performing series of predictions is done in case the fusion deteriorates the performance.

#LIBRARY DEPENDENCIES

These are the following library you need to install to use these scripts:
- Numpy
- Scipy
- Matplotlib
- Liac-arff (2.1.1)
- Sklearn (0.19.1)

#HOW TO SET UP

First of all you must set all the variables in the Config/Config.py file:
- Folder containing the dataset (the one from the AVEC 2018 GES data repository with exact structure and name of the files)
- Folder containing the version of the gold-standard to use
- Number of threads available to run the emotion recognition system.
Please be sure to put a / at the end of each folder.
The base folders will be those of the AVEC_2018 GES repository; structure and name of the files must be preserved.

#HOW TO RUN

To replicate the generation of the Gold Standard from the individual ratings (recreating in the GS Folder the baseline Gold Standard):
- Go in the GoldStandardCreation folder
- Type "python GSCreation.py"
- Results will go to "gs_created" folder.

To perform monomodal/multimodal emotion recognition:
- Go in the Pred folder
- Type "python Pred.py ARGS"
- If you don't put any argument the multimodal prediction will launch.
- If you don't put "full" or "--full", the predictions will only use SVR
- Otherwise you can put a number for the modality (for the number correspondance, type "python Pred.py help")
- You can add the option "debug" or "--debug" if you want a higher verbose level
- You can add "full" or "--full" if you want to test linear model on the predictions (the script may take up to 24h)

#HOW TO SET UP YOUR SCRIPT WITH YOUR GOLD STANDARD

- Put your folder containing your GS in the "labels" folder; be sure to have two separate folders: "arousal" and "valence", and that the base name of each arff file is "partition_number.arff" (ex : dev_1.arff)
- Go in the config.py file and put the name of your folder 
- Run prediction with the Pred.py script

#HOW TO INSTALL ON WINDOWS (tested on Windows 7 - 64bits)

- Download python2.7, you can get it here : https://www.python.org/downloads/release/python-2715/
- Take the "Windows x86-64 MSI installer"
- After installation, environment variables must be set, there is a tutorial here : https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
  You must set the variable "PYTHON_HOME" to the path where python is and to the var "path", you must add "%PYTHON_HOME%;%PYTHON_HOME%\Scripts\;"
- Install pip, download link here : https://bootstrap.pypa.io/get-pip.py
- Open a CMD in administrator mode
- Go to the folder where get-pip.py is (cd PATH)
- Run "python get-pip.py", this will install it (Environment variables should be set for pip but if you can't lauch it from everywhere you need to add these too)
- Install the libraries : "python -m pip install --user numpy scipy matplotlib liac-arff sklearn" on cmd
- Go in the liblinear-2.20 folder in the repository, you need to compile it
- Then go to the python folder within liblinear and compile it too
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL ON LINUX (tested on Ubuntu 16.04/14.04)

- First install python2.7 : "sudo apt-get install python"
- Install pip : "sudo apt-get install pip"
- Install the libraries : "python -m pip install --user numpy scipy matplotlib liac-arff sklearn"
- Go in the liblinear-2.20 folder in the repository, you need to compile it (make)
- Then go to the python folder within liblinear and compile it too (make)
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL ON MACOS (not tested)

- Feedbacks welcome!
