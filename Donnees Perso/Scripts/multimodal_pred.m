function multimodal_pred(AVEC_2016_path,output_path,modalities,emo_dim,weka_path)

%commands for weka
weka_train='weka.classifiers.functions.LinearRegression -S 1 -C -R 1.0E-8 -v -no-cv -c "last" ';
weka_test='weka.classifiers.functions.LinearRegression -v -no-cv -p 0 -c "last" ';
weka_decimals='-classifications "weka.classifiers.evaluation.output.prediction.CSV -decimals 9" ';

Nmod=length(modalities);
Ndim=length(emo_dim);

%parameters for post-processing
Nw=500;

%build 3 fusion models
%1) audio-ecg (when frames are missing for both video and eda)
%2) audio-ecg-eda (when frames are missing for video)
%3) audio-ecg-eda-video (when all frames are available)

%group predictions
pred_dev=cell(Nmod,Ndim);
% pred_test=cell(Nmod,Ndim);
frames_video_dev=cell(Nmod,Ndim);
% frames_video_test=cell(Nmod,Ndim);
gs_dev=cell(1,Ndim);
% gs_test=cell(1,Ndim);
for m=1:Nmod,
    for dim=1:Ndim,
        data=load(fullfile(AVEC_2016_path,'unimodal_pred_LIBLINEAR',modalities{m},['final_results_' emo_dim{dim} '.mat']));
        if m==1,
            gs_dev{dim}=data.gs_dev;
%             gs_test{dim}=data.gs_test;
        end
        pred_dev{m,dim}=data.pred_dev_post;
%         pred_test{m,dim}=data.pred_test_post;
        if m==2 || m==3,
            frames_video_dev{m,dim}=data.frames_video_dev;
%             frames_video_test{m,dim}=data.frames_video_test;
        end
    end
end

%merge video frames for appearance and geometric
frames_video_dev_merged=cell(1,Ndim);
for d=1:Ndim,
    frames_video_dev_merged{d}=frames_video_dev{2,d} | frames_video_dev{3,d};
end
% frames_video_test_merged=cell(1,Ndim);
% for d=1:Ndim,
%     frames_video_test_merged{d}=frames_video_test{2,d} | frames_video_test{3,d};
% end

%% build model (1) - audio-ecg-hrhrv

fprintf('\t -> Build fusion model 1/3 - audio-ecg-hrhrv (missing eda and video frames)\n')

m=[1 4 5];
pred_dev_audio_ecg=cell(1,Ndim);
% pred_test_audio_ecg=cell(1,Ndim);
CCC_dev_audio_ecg=cell(1,Ndim);
% CCC_test_audio_ecg=cell(1,Ndim);
for d=1:Ndim,
    
    %data
    pred_dev_local=[pred_dev{m,d}]';
%     pred_test_local=[pred_test{m,d}]';
    gs_dev_local=gs_dev{d}';
%     gs_test_local=gs_test{d}';
    
    %write data in arff
    devarff=fullfile(output_path,'data_dev.arff');
%     testarff=fullfile(output_path,'data_test.arff');
    modfile=fullfile(output_path,'linreg.model');
    modread=fullfile(output_path,['audio_ecg_linreg_model_' emo_dim{d} '.txt']);
    output_dev=fullfile(output_path,'output_dev.csv');
%     output_test=fullfile(output_path,'output_test.csv');
    arffwrite(devarff,'header',[modalities(m) 'gold_standard'],[pred_dev_local;gs_dev_local])
%     arffwrite(testarff,'header',[modalities(m) 'gold_standard'],[pred_test_local;gs_test_local])
    
    %learn model
    unix(['java -classpath "' weka_path '" ' weka_train ' -t "' devarff '" -d "' modfile '" > ' modread]);
    %apply model on dev data
    unix(['java -classpath "' weka_path '" ' weka_test ' -T "' devarff '" -l "' modfile '" ' weka_decimals ' > ' output_dev]);
%     %apply model on test data
%     unix(['java -classpath "' weka_path '" ' weka_test ' -T "' testarff '" -l "' modfile '" ' weka_class ' > ' output_test]);
    
    %learn the post processings and evaluate performance
    FID=fopen(output_dev);
    data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
    fclose(FID);
    %2->gs, 3->pred
    [CCC_dev,best_param,pred_post_dev] = predpostproc_train(data{3},data{2},Nw);
    
%     %apply post processing on test
%     FID=fopen(output_test);
%     data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
%     fclose(FID);
%     [CCC_test,pred_post_test] = predpostproc_test(data{3},data{2},best_param);
    
    %save results
    pred_dev_audio_ecg{d}=pred_post_dev;
%     pred_test_audio_ecg{d}=pred_post_test;
    CCC_dev_audio_ecg{d}=CCC_dev;
%     CCC_test_audio_ecg{d}=CCC_test;
    
    %delete temporary files
%     delete(devarff,testarff,modfile,output_dev,output_test);
    delete(devarff,modfile,output_dev);
end


%% build model (2) - audio-ecg-eda

fprintf('\t -> Build fusion model 2/3 - audio-ecg-hrhrv-eda-scl-scr (missing video frames)\n')

m=[1 4 5 6 7 8];
pred_dev_audio_ecg_eda=cell(1,Ndim);
% pred_test_audio_ecg_eda=cell(1,Ndim);
CCC_dev_audio_ecg_eda=cell(1,Ndim);
% CCC_test_audio_ecg_eda=cell(1,Ndim);
for d=1:Ndim,
    
    %data
    pred_dev_local=[pred_dev{m,d}]';
%     pred_test_local=[pred_test{m,d}]';
    gs_dev_local=gs_dev{d}';
%     gs_test_local=gs_test{d}';
    
%     %remove test data from subject 7 (due to EDA)
%     ind=logical(pred_test_local(end,:)~=0);
%     pred_test_local=pred_test_local(:,ind);
%     gs_test_local=gs_test_local(:,ind);
    
    %write data in arff
    devarff=fullfile(output_path,'data_dev.arff');
%     testarff=fullfile(output_path,'data_test.arff');
    modfile=fullfile(output_path,'linreg.model');
    modread=fullfile(output_path,['audio_ecg_eda_linreg_model_' emo_dim{d} '.txt']);
    output_dev=fullfile(output_path,'output_dev.csv');
%     output_test=fullfile(output_path,'output_test.csv');
    arffwrite(devarff,'header',[modalities(m) 'gold_standard'],[pred_dev_local;gs_dev_local])
%     arffwrite(testarff,'header',[modalities(m) 'gold_standard'],[pred_test_local;gs_test_local])
    
    %learn model
    unix(['java -classpath "' weka_path '" ' weka_train ' -t "' devarff '" -d "' modfile '" > ' modread]);
    %apply model on dev data
    unix(['java -classpath "' weka_path '" ' weka_test ' -T "' devarff '" -l "' modfile '" ' weka_decimals ' > ' output_dev]);
%     %apply model on test data
%     unix(['java -classpath "' weka_path '" ' weka_test ' -T "' testarff '" -l "' modfile '" ' weka_class ' > ' output_test]);
    
    %learn the post processings and evaluate performance
    FID=fopen(output_dev);
    data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
    fclose(FID);
    %2->gs, 3->pred
    [CCC_dev,best_param,pred_post_dev] = predpostproc_train(data{3},data{2},Nw);
    
%     %apply post processing on test
%     FID=fopen(output_test);
%     data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
%     fclose(FID);
%     [CCC_test,pred_post_test] = predpostproc_test(data{3},data{2},best_param);
    
    %save results
    pred_dev_audio_ecg_eda{d}=pred_post_dev;
%     pred_test_audio_ecg_eda{d}=pred_post_test;
    CCC_dev_audio_ecg_eda{d}=CCC_dev;
%     CCC_test_audio_ecg_eda{d}=CCC_test;
    
    %delete temporary files
%     delete(devarff,testarff,modfile,output_dev,output_test);
    delete(devarff,modfile,output_dev);
end

%% build model (3) - all modalities

fprintf('\t -> Build fusion model 3/3 - all modalities\n')
m=1:Nmod;
pred_dev_all=cell(1,Ndim);
% pred_test_all=cell(1,Ndim);
CCC_dev_all=cell(1,Ndim);
% CCC_test_all=cell(1,Ndim);
for d=1:Ndim,
    
    %data
    pred_dev_local=[pred_dev{m,d}]';
%     pred_test_local=[pred_test{m,d}]';
    gs_dev_local=gs_dev{d}';
%     gs_test_local=gs_test{d}';
    
    %filter dev and test data according to video data
    pred_dev_local=pred_dev_local(:,frames_video_dev_merged{d});
    gs_dev_local=gs_dev_local(frames_video_dev_merged{d});
%     pred_test_local=pred_test_local(:,frames_video_test_merged{d});
%     gs_test_local=gs_test_local(frames_video_test_merged{d});
    
%     %remove test data from subject 7 (due to EDA)
%     ind=logical(pred_test_local(end,:)~=0);
%     pred_test_local=pred_test_local(:,ind);
%     gs_test_local=gs_test_local(:,ind);
    
    %write data in arff
    devarff=fullfile(output_path,'data_dev.arff');
%     testarff=fullfile(output_path,'data_test.arff');
    modfile=fullfile(output_path,'linreg.model');
    modread=fullfile(output_path,['all_linreg_model_' emo_dim{d} '.txt']);
    output_dev=fullfile(output_path,'output_dev.csv');
%     output_test=fullfile(output_path,'output_test.csv');
    arffwrite(devarff,'header',[modalities(m) 'gold_standard'],[pred_dev_local;gs_dev_local])
%     arffwrite(testarff,'header',[modalities(m) 'gold_standard'],[pred_test_local;gs_test_local])
    
    %learn model
    unix(['java -classpath "' weka_path '" ' weka_train ' -t "' devarff '" -d "' modfile '" > ' modread]);
    %apply model on dev data
    unix(['java -classpath "' weka_path '" ' weka_test ' -T "' devarff '" -l "' modfile '" ' weka_decimals ' > ' output_dev]);
%     %apply model on test data
%     unix(['java -classpath "' weka_path '" ' weka_test ' -T "' testarff '" -l "' modfile '" ' weka_class ' > ' output_test]);
    
    %learn the post processings and evaluate performance
    FID=fopen(output_dev);
    data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
    fclose(FID);
    %2->gs, 3->pred
    [CCC_dev,best_param,pred_post_dev] = predpostproc_train(data{3},data{2},Nw);
    
%     %apply post processing on test
%     FID=fopen(output_test);
%     data=textscan(FID,'%f %f %f %f','Delimiter',',','HeaderLines',5);
%     fclose(FID);
%     [CCC_test,pred_post_test] = predpostproc_test(data{3},data{2},best_param);
    
    %save results
    pred_dev_all{d}=pred_post_dev;
%     pred_test_all{d}=pred_post_test;
    CCC_dev_all{d}=CCC_dev;
%     CCC_test_all{d}=CCC_test;
    
    %delete temporary files
%     delete(devarff,testarff,modfile,output_dev,output_test);
    delete(devarff,modfile,output_dev);
end

%% combine fusion models
pred_comb_dev=cell(1,Ndim);
% pred_comb_test=cell(1,Ndim);
CCC_dev_comb=zeros(1,Ndim);
% CCC_test_comb=zeros(1,Ndim);
for d=1:Ndim,
    %%%dev%%%
    %include audio-ecg-eda (always present)
    pred_comb_dev{d}=pred_dev_audio_ecg_eda{d};
    %add predictions from all
    pred_comb_dev{d}(frames_video_dev_merged{d})=pred_dev_all{d};
    CCC_dev_comb(d)=CCC_calc(pred_comb_dev{d},gs_dev{d});
    
%     %%%test%%%
%     %include audio-ecg (always present)
%     pred_comb_test{d}=pred_test_audio_ecg{d};
%     %add predictions from audio-ecg-eda
%     ind=logical(pred_test{end,d});
%     pred_comb_test{d}(ind)=pred_test_audio_ecg_eda{d};
%     %add predictions from all
%     pred_comb_test{d}(ind&frames_video_test_merged{d})=pred_test_all{d};
%     CCC_test_comb(d)=CCC_calc(pred_comb_test{d},gs_test{d});

%     fprintf('\t-> %s, (dev) CCC=%3.3f, (test) CCC=%3.3f\n',emo_dim{d},CCC_dev_comb(d),CCC_test_comb(d))
    fprintf('\t-> %s, (dev) CCC=%3.3f\n',emo_dim{d},CCC_dev_comb(d))
end
