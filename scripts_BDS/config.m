%only the following two lines need to be setup
%
%path of the main directory of the AVEC 2018 Bipolar Disorder Sub-challenge
%=> must be changed to your own folder
mainpath='/Users/ringeval/Documents/Databases/AVEC_2018/BDS/official_package';

%path of the liblinear library - https://github.com/cjlin1/liblinear
%=> must be changed to your own folder
%=> liblinear needs to be compiled first with MATLAB using mex - see readme in liblinear
libsvm_path='/Users/ringeval/Documents/Applications/liblinear/matlab';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%add liblinear path to MATLAB
addpath(libsvm_path);

%commands for libsvm
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05 0.1 0.2 0.5 1];Nc=length(C);
solver_val=0:7;Nsol=length(solver_val);

%path for baseline features
basefeatpath=fullfile(mainpath,'baseline_features');

%create path containing a posteriori classification probabilities
probas_path=fullfile(mainpath,'probas');
if isempty(dir(probas_path)),
    mkdir(mainpath,'probas');
end

%number of classes
Nclass=3;

%number of attributes in csv feature file
Natt_MFCCs=41;
Natt_eGeMAPS=88;
Natt_BoW=1000;
Natt_DeepSpectrum=4096;
Natt_FAUs=24;

%name of audio representations
Nar=4;
audio_rep=cell(1,Nar);
audio_rep{1}='prob_audio_mfcc';
audio_rep{2}='prob_audio_eGeMAPS';
audio_rep{3}='prob_audio_BoAW';
audio_rep{4}='prob_audio_DeepSpectrum';

%name of video representations
Nvr=2;
video_rep=cell(1,Nvr);
video_rep{1}='prob_video_FAUs';
video_rep{2}='prob_video_BoVW';

%list of partitions
Np=2;%Np=3;
part=cell(1,Np);
part{1}='train';
part{2}='dev';
% part{3}='test';

%load labels, instance name
% fid=fopen(fullfile(mainpath,'labels_metadata_test_confidential.csv'));
fid=fopen(fullfile(mainpath,'labels_metadata.csv'));
data=textscan(fid,'%s %s %d %s %d %d %s','HeaderLines',1,'Delimiter',',');
fclose(fid);
Nlines=size(data{1},1);
instancename=data{1};label=data{end-1};partfile=zeros(1,Nlines);
for l=1:Nlines,
    for p=1:Np,
        if strfind(instancename{l},part{p}),
            partfile(l)=p;
            break; 
        end
    end
end
%sort instances by partition
labels=cell(1,Np);
parinstname=cell(1,Np);
for p=1:Np,
    indpart=find(partfile==p);
    parinstname{p}=instancename(indpart);
    [name,ind]=sort(parinstname{p});
    labels{p}=double(label(indpart(ind)))';
    parinstname{p}=name;
end