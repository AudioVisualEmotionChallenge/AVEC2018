# Baseline scripts for the AVEC 2018 GES Sub-challenge

#GENERAL DESCRIPTION OF THE SYSTEM

The scripts allow to train and optimise a multimodal emotion recognition system on the RECOLA dataset to predict emotion labels, either provided in the data package, or by the participant; predictions are made every 400 ms. Performance is measured with the concordance correlation coefficient between the gold-standard and the series of predictions (average of the CCC over the recordings) obtained on the development and test partitions. Results on the test partition, which will serve for ranking the submissions, cannot be reproduced since test labels are not available, despite we provide the scripts on test for full transparency. 

#AUDIOVISUAL FEATURES (external access)

The emotion recognition system exploits audio, video and physiological signals, with different representations that are either hand-crafted or learned in an unsupervised way. More precisely, audio features include the eGeMAPS hand-crafter feature set (openSMILE; sliding window with a size ranging from 3 seconds to 9 seconds), Bags-of-Audio-Words (openXBOW; codebook size is 100, soft assignment, words computed from 12 MFCCs + log energy, with delta and delta-delta and with the same sliding windows as used for eGeMAPS), and a representation obtained with unsupervised based deep learning (auDeep; sparse features obtained by the activation function of each neuron of the hidden to last layer connection of a deep autoencoder). Video features include appearance and geometric based features (same set as used in the AVEC 2016 MASC Sub-challenfge), facial action units (openFACE; intensity of 17 FAUs), and Bags-of-Video-Words computed from those FAUs (oenXBOW; same configuration as for Bags-of-Audio-Words), all computed on sliding windows with the same range of duration as used for audio data. Physiological features are the same as used in the AVEC 2016 MASC Sub-challenge.

#SYSTEM ARCHITECTURE

The architecture of the recognition system is hierarchical and starts with a series of models learned on the training set for each modality and each representation. The models include Support Vector Machines (liblinear with L2-L2 dual form of the regression solver), and generalised linear models (ridge regression, lasso, multi-task lasso, elastic net, and multi-task elastic net) from the scikit machine learning toolbox. Optimisation of each model is performed on the development partition by performing a grid-search over the following parameters: window size, time delay uniformly applied to the gold-standard, regularisation coefficients (complexity for SVR, alpha for generalised linear models) and post-processing parameters (bias and scaling factor); features of each set (training, development and test) are standardised using the first two statistical moments computed on the training set. Selection of the best model and its corresponding hyper-parameters is done on the development partition. Two different late fusion strategies are then compared: one that fuses all predictions obtained by the different modalities (audio, video, and physiogical) and their corresponding representation (functionals, bags-of-words, and unsupervised deep learning), and another that fuses each represantation of the different modalities, and then the obtained series of predictions over the modalities. Optimisation of the regression models used for the fusion processes includes only the regularisation parameter alpha. Replication of the best performing series of predictions is done in case the fusion deteriorates the performance.

#LIBRARY DEPENDENCIES

These are the following library you need to install to use the baseline scripts for the AVEC 2018 GES:
- Numpy
- Scipy
- Matplotlib
- Liblinear (2.20)
- Liac-arff (2.1.1)
- Sklearn (0.19.1)

#HOW TO INSTALL ON LINUX (tested on Ubuntu 14.04 and 16.04)

- Install python2.7: "sudo apt-get install python"
- Install pip: "sudo apt-get install pip"
- Install the libraries: "python -m pip install --user numpy scipy matplotlib liac-arff sklearn"
- Install liblinear (pip has not the latest version): http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Unzip liblinear and put the address to the python folder within
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL ON WINDOWS (tested on Windows 7 - 64bits)

- Download python2.7, https://www.python.org/downloads/release/python-2715/
- Install python using "Windows x86-64 MSI installer"
- Set up environment variables following this tutorial: https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
- Install pip: https://bootstrap.pypa.io/get-pip.py
- Open a CMD in administrator mode
- Go to the folder where get-pip.py is and run "python get-pip.py", this will install it. Environment variables should be set for pip but if you can't lauch it from everywhere you need to add these too.
- Install the libraries: "python -m pip install --user numpy scipy matplotlib liac-arff sklearn" on cmd
- Install liblinear (pip has not the latest version): http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+zip
- Unzip liblinear and put the address to the python folder within
- Set up the project (#HOW TO SET UP)

#HOW TO INSTALL ON MACOS (not tested)

-  feedbacks welcome!

#HOW TO SET UP

First of all you must set the three variables in the Config/Config.py file: (i) folder containing the dataset (the one from the AVEC 2018 GES data repository with exact structure and name of the files), (ii) version of the gold-standard to use, and (iii) number of threads available to run the emotion recognition system.

#HOW TO RUN

For Gold Standard Creation (recreating in the GS Folder the baseline Gold Standard) :
- Go in the GoldStandardCreation folder
- Type "python GSCreation.py"
- Results will go to "gs_created" folder.
For the Audio Prediction :
- Go in the AudioPred folder
- Type "python Pred.py ARGS"
- If you don't put any argument the multimodal prediction will launch.
- Otherwise you can put a number for the modality (for the number correspondance, type "python AudioPred.py help")



