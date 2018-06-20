# AVEC_2018
Baseline scripts of the 8th Audio/Visual Emotion Challenge

## Structure:

## extract_features/:

Baseline scripts (Python 2) for audio/visual features extraction from audio/visual recordings; main functions:

* extract\_audio\_features.py: Extract acoustic features over time (either eGeMAPS LLDs or MFCCs + delta + acceleration) using openSMILE.

* extract\_video\_features.py: Extract visual features (FAU likelihoods) for all video files.

* generate\_xbow.py: Generate Bag-of-Words representations from audio or visual descriptors.

See the readme.md in the folder for setup and informations.

## scripts_BDS/:

Baseline scripts (Matlab) for the Bipolar Disorder Sub-Challenge (BDS); main functions:

* main.m: Reproduce all baseline recognition results.

* config.m: Configuration file for the scripts (path to data and liblinear).

See the readme_BDS.md in the folder for setup and informations.

## scripts_CES/:

Baseline scripts (Python 2) for the Cross-cultural Emotion Sub-Challenge (CES); main functions:

* baseline\_lstm.py: Perform training of a 2-layer LSTM on the XBOW features and save predictions.  

* calc\_scores.py: Calculate Concordance Correlation Coefficient (CCC), Pearson's Correlation Coefficient (PCC) and Mean Squared Error (MSE) on the concatenated predictions. Note: Only the CCC is taken into account as the official metric for the challenge.

See the readme_CES.md in the folder for setup and informations.

## scripts_GES/:

Baseline scripts (Python 2) for the Gold-standard Emotion Sub-Challenge (GES); main functions:

* GoldStandardCreation/GSCreation.py: Create gold-standard from indivudal ratings of emotion labels.

* Pred/Pred.py: Run multimodal emotion recognition based on a given gold-standard.

* Config/Config.py: Configuration file for all scripts.

See the readme_GES.md in the folder for setup and informations

