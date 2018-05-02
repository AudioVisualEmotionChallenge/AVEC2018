%This is the script to reproduce the baseline score on AVEC 2016 MASC.
%All features and ratings must be located in the same directory
%Required:
%   MATLAB (R2014b or higher + statistical toolbox + parallel toolbox)
%   LIBLINEAR (2.1 or higher)
%   Weka (3.7 or higher)

%All processes take around 133 minutes (2h13) on a i7-4770K CPU (3.5 GHz)

clear all, %#ok<CLSCR>
clc

%% path to data and softwares

%path containing features and gold standard
AVEC_2016_path='D:\Databases\RECOLA_AVEC_2016\Baseline\Data\';
gs_path=fullfile(AVEC_2016_path,'ratings_gold_standard');

%path containing LIBLINEAR for matlab (monomodal predictions)
libsvm_path='C:\Users\rin\Documents\Applications\liblinear-2.1\matlab\';
addpath(libsvm_path);

%path containing WEKA (multimodal predictions)
weka_path='C:\Program Files\Weka-3-7\weka.jar';

%% declaration of constants

%list of modalities
Nmod=8;
modalities=cell(1,Nmod);
modalities{1}='audio';
modalities{2}='video_appearance';
modalities{3}='video_geometric';
modalities{4}='ECG';
modalities{5}='HRHRV';
modalities{6}='EDA';
modalities{7}='SCL';
modalities{8}='SCR';

%emotional dimensions
Ndim=2;
emo_dim=cell(1,Ndim);
emo_dim{1}='arousal';
emo_dim{2}='valence';

%standardisation approach: online (1) / speaker dependent (2)
stand_app=zeros(Ndim,Nmod);
stand_app(1,:)=[1 2 2 2*ones(1,5)];
stand_app(2,:)=[1 1 1 2*ones(1,5)];

%sampling period of features
Ts=0.04; %40 ms

%delay in seconds to apply on the gold standard
delays=0:0.4:8;

%% launch parallel toolbox if available
fprintf('-> Starting parallel toobox... \n')
poolobj=parpool;
if poolobj.Connected,
    fprintf('\t-> Connected to %d workers\n',poolobj.NumWorkers)
else
    fprintf('\t Parallel toolbox is not available, all jobs will be running on a single core\n')
end
fprintf('\n');

%% add shifted version of gold-standard to features
fprintf('-> Add delayed version of gold-standard to features... ')
tic;
if poolobj.Connected,
    parfor m=1:Nmod,
        add_gs(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim,Ts,gs_path,delays);
    end
else
    for m=1:Nmod,
        add_gs(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim,Ts,gs_path,delays);
    end
end
t=toc;
fprintf('done in %f s\n\n',t);
%8 min

%% concatenate recordings per partition (train / dev)
fprintf('-> Concatenate features per partition... ')
tic;
if poolobj.Connected,
    parfor m=1:Nmod,
        conc_arff(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim);
    end
else
    for m=1:Nmod,
        conc_arff(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim);
    end
end
t=toc;
fprintf('done in %f s\n\n',t);
%7 min

%% standardise features
fprintf('-> Standardise features... ')
tic;
if poolobj.Connected,
    parfor m=1:Nmod,
        stand_feat(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim,stand_app(:,m));
    end
else
    for m=1:Nmod,
        stand_feat(fullfile(AVEC_2016_path,['features_' modalities{m}]),emo_dim,stand_app(:,m));
    end
end
t=toc;
fprintf('done in %f s\n\n',t);
%7 min

%% unimodal prediction to optimise the delay
%
%please note that performance reported here may differ from the final results,
%because we shift back in time here the gold-standard (last value of each 
%recording is duplicated), whereas predictions are shifted forward in time for
%the final evaluation (first frame is duplicated)
%
fprintf('-> Monomodal prediction (optimisation of the delay on dev)...\n')
tic;
for m=1:Nmod,
    fprintf('\t -> %s\n',modalities{m});
    
    feat_path=fullfile(AVEC_2016_path,['features_' modalities{m}]);
    output_path=fullfile(AVEC_2016_path,'unimodal_pred_LIBLINEAR',modalities{m});
    if isempty(dir(output_path)),
        mkdir(AVEC_2016_path,fullfile('unimodal_pred_LIBLINEAR',modalities{m}));
    end
    
    %perform prediction
    liblinear_pred(feat_path,output_path,emo_dim,delays,poolobj.Connected);
end
t=toc;
fprintf('\ndone in %f s\n\n',t);
%107 min

%% final unimodal prediction
fprintf('-> Final monomodal prediction (predictions shifted forward)...\n')
tic;
for m=1:Nmod,
    fprintf('\t -> %s\n',modalities{m});
    
    feat_path=fullfile(AVEC_2016_path,['features_' modalities{m}]);
    output_path=fullfile(AVEC_2016_path,'unimodal_pred_LIBLINEAR',modalities{m});
    
    final_unimodal_pred(AVEC_2016_path,feat_path,output_path,emo_dim,delays,m,Ts);
end
t=toc;
fprintf('\ndone in %f s\n\n',t);
%2 min

%% multimodal prediction
fprintf('-> Multimodal prediction (decision fusion)... \n')
tic;
output_path=fullfile(AVEC_2016_path,'multimodal_pred_WEKA');
if isempty(dir(output_path)),
    mkdir(AVEC_2016_path,fullfile('multimodal_pred_WEKA'));
end
multimodal_pred(AVEC_2016_path,output_path,modalities,emo_dim,weka_path);
t=toc;
fprintf('\ndone in %f s\n',t);
%2 min

%% shut down parallel toolbox
delete(gcp);