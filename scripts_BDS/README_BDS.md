# Baseline scripts of the AVEC 2018 BDS

The scripts reproduce the baseline results of the AVEC 2018 BDS.

Participants of the BDS have to classify patients suffering from bipolar disorder into remission, hypo-mania, and mania, following the young mania rating scale, from audio-visual recordings of structured interviews (BD corpus). 

The official metric to evaluate the performance is the unweighted average recall: 

	UAR = 1/3 * (recall(remission) + recall(hypo-mania) + recall(mania))

## SYSTEM ARCHITECTURE

The baseline recognition system exploits audio and video signals, with different representations that are either hand-crafted or learned in an unsupervised way. The architecture of the recognition system is a simple late fusion of the best performing audio and video representations using linear Support Vector Regression. 

For audio data, MFCCs (frame level), eGeMAPS (turn level based on post-processed VAD obtained with LSTM RNN), Bag-of-Audio-Words (window sise of 2s, hop-size of 1s, 20 soft assignments, codebook size of 1000) and Deep Spectrum representations are used for learning SVMs. 

For video data, functionals (mean, standard-deviation, relative position of maximum) of FAUs (session level) and Bag-of-Video-Words (window sise of 11s, hop-size of 1s, 20 soft assignments, codebook size of 1000) are exploited.

Standardisation is performed only on the sets of functionals (eGeMAPS for audio and FAUs for video); Bag-of-Words and Deep Spectrum representations are processed as they are (values of log-frequency, and activation function are naturally in the appropriate range for machine learning). 

For frame based features, the final decision on the session is taken by majority voting from the predictions. Performance (%UAR) on the development set is as follows (chance level is 33.33):

(DEV) MFCCs: 49.47, eGeMAPS: 55.03, BoAW: 55.03, DeepSpectrum: 58.20, FAUs: 55.82, BoVW: 55.82

Performance on the test set for the best two representations for audio and the best representation for video, respectively, is as follows (supervised representation was prefered over semi-supervised, i.e., BoW, in cases of a draw):

(TEST) eGeMAPS: 50.00, Deep Spectrum: 44.44, FAUs: 46.30

Fusion of each best audio representation with the one obtained from video data, which is performed by another SVMs model learned on the a posteriori probabilities estimated from the frame-level or turn-level decisions, or by a logistic function for the session-level features, i.e., FAUs, performs as follows:

(DEV)  eGeMAPS + FAUs: 60.32, Deep Spectrum + FAUs: 63.49

(TEST) eGeMAPS + FAUs: 57.41, Deep Spectrum + FAUs: 44.44


## LIBRARY DEPENDENCIES

Besides using Matlab (or Octave), the liblinear library (https://github.com/cjlin1/liblinear) needs to be installed to use these scripts.

## HOW TO SET UP

You only need to provide the local folder containing the baseline scripts and the baseline features, and the path to the liblinear library in the Config.m file.

Architecture of the files (name must be preserved) must be:
local_folder/
	baseline_features/
	scripts_BDS/
	labels_metadata.csv

## HOW TO RUN

To replicate the baseline results, simply run the main.m file.
Both modality and representation specific results can be replicated independently using the corresponding script; classification_audio/video/audiovideo_MFCCs/eGeMAPS/DeepSpectrum/AUs/BoW_frame/turn/session.m; the script running fusion must be performed after the replication of the modality dependent results as it requires the a posteriori probabilities.
