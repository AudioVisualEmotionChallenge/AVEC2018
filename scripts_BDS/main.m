%main baseline script of the AVEC 2018 BDS Sub-challenge reproducing unimodal recognition results

clc;fprintf('AVEC 2018 Bipolar Disorder Sub-challenge baseline recognition system (Mania/Hypomania/Remission)\n\n')

%run configuration file
config;

%run audio MFCC
fprintf('* Audio: MFCCs (0-12, +delta, +delta-delta, majority voting)\n')
classification_audio_MFCCs_frame

%run audio eGeMAPS
fprintf('\n* Audio: eGeMAPS (functionals per turn, majority voting)\n')
classification_audio_eGeMAPS_turn

%run audio BoW
fprintf('\n* Audio: Bag-of-Words (log-frequency of 1000 words with 20 assignments, majority voting)\n')
featpath=fullfile(basefeatpath,'features_audio_BoAW_A20_C1000');ws=2;audio=1;%#ok<*NASGU> %best config for audio
classification_audiovideo_BoW_window

% run audio Deep Spectrum
fprintf('\n* Audio: Deep Spectrum (DNN''s activation functions per frame, majority voting)\n')
classification_audio_DeepSpectrum_frame

%run video FAUs
fprintf('\n* Video: Facial action units (stats on FAUs per session)\n')
classification_video_AUs_session

%run video BoW
fprintf('\n* Video: Bag-of-Words (log-frequency of 1000 words with 20 assignments, majority voting)\n')
featpath=fullfile(basefeatpath,'features_video_BoVW_A20_C1000');ws=11;audio=0;%best config for video
classification_audiovideo_BoW_window

%run fusion
fusion