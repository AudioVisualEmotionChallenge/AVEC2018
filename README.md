# AVEC_2018
Baseline scripts of the 8th Audio/Visual Emotion Challenge

## Structure: ##

scripts_BDS/:  

Baseline scripts (Python 2) for the Bipolar Disorder Sub-Challenge (BDS) - coming soon!

scripts_CES/:  

Baseline scripts (Python 2) for the Cross-cultural Emotion Sub-Challenge (CES)

* baseline\_lstm.py: The deep learning framework Keras is required to run the CES baseline scripts. The baseline scripts have been tested with Python 2.7 and Tensorflow as backend.  
To run the baseline, you need to run the script generate\_xbow.py first. This script generates bag-of-audio-words and bag-of-visual-words (XBOW) features in the folders audio\_features\_xbow/ and visual\_features\_xbow/  
Then, run the script baseline\_lstm.py. It trains a 2-layer LSTM on the XBOW features and writes predictions on the test sets into the folder predictions/, for the model achieving the best performance in terms of CCC on the development set (independently for each dimension).

* calc\_scores.py: Calculate Concordance Correlation Coefficient (CCC), Pearson's Correlation Coefficient (PCC) and Mean Squared Error (MSE) on the concatenated predictions. Note: Only the CCC is taken into account as the official metric for the challenge.

* CES\_data.py: Python module to load the feature files of all partitions (used by baseline\_lstm.py).

* extract\_audio\_features.py: Extract acoustic features over time (either eGeMAPS LLDs or MFCCs + delta + acceleration) for all audio files in the folder 'audio/'. Features are stored in the folder 'audio_features/'. The feature script to be extracted needs to be configured in line 11.

* extract\_video\_features.py: Extract visual features (FAU likelihoods) for all video files in the folder 'video/'. Features are stored in the folder 'visual_features/'.

* generate\_xbow.py: Extract bag-of-audio-words (BoAW) and bag-of-video-words (BoVW) features from the respective low-level descriptors configured in lines 13 and 14. This script uses the tool openXBOW (see below).

* openXBOW.jar: The openXBOW (Passau Open-Source Crossmodal Bag-of-Words) Toolkit, latest version 1.0. Available here: https://github.com/openXBOW/openXBOW

* read\_csv.py, write\_csv.py: auxiliary scripts


scripts_GES/:

Baseline scripts (Python 2) for the Gold-standard Emotion Sub-Challenge (GES)

* GoldStandardCreation/GSCreation.py: Create gold-standard from indivudal ratings of emotion labels.

* Pred/Pred.py: Run multimodal emotion recognition based on a given gold-standard.

* Config/Config.py: Configuration file for all scripts.

See the readme_GES.md in the folder for setup and informations

