function final_unimodal_pred(AVEC_2016_path,feat_path,output_path,emo_dim,delays,m,Ts)

%commands for libsvm
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1];
Nc=length(C);
solver_val=12;%L2L2_dual

Ndel=length(delays);
Ndim=length(emo_dim);
Nframes=7501;
Nsub=9;

%parameters for post-processing
Nw=500;

%loop on emotional dimensions
for dim=1:Ndim,
    
    if isempty(dir(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']))),
        
        %read optimisation results
        data=load(fullfile(output_path,['dev_all_results_' emo_dim{dim}]));
        CCC_valid=data.CCC_valid;
        
        %parse best complexity and delay
        best_CCC=-2;
        for c=1:Nc,
            for del=1:Ndel,
                if CCC_valid(c,del)>best_CCC,
                    best_CCC=CCC_valid(c,del);
                    best_del=del;
                    best_C=num2str(C(c));
                end
            end
        end
        
        %read features
        [features_train,gs_train] = read_arff(fullfile(feat_path,emo_dim{dim},'stand_train.arff'),Ndel);
        [features_dev,gs_dev] = read_arff(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'),Ndel);
%         [features_test,gs_test] = read_arff(fullfile(feat_path,emo_dim{dim},'stand_test.arff'),Ndel);
        
        %remove frametime
        features_train=features_train(:,2:end);
        features_dev=features_dev(:,2:end);
%         features_test=features_test(:,2:end);
        
        %force to zero NaN values
        features_train(logical(isnan(features_train)))=0;
        features_dev(logical(isnan(features_dev)))=0;
%         features_test(logical(isnan(features_test)))=0;
        
        %sparse format
        features_train=sparse(features_train);
        features_dev=sparse(features_dev);
%         features_test=sparse(features_test);
        
        %learn model on train
        options=['-s ' num2str(solver_val) ' -c ' best_C ' -B 1 -q'];
        model=train(gs_train(:,best_del),features_train,options);
        
        %predict on dev with model on train
        pred_dev=predict(gs_dev(:,best_del),features_dev,model,'-q');
        
        %learn the post processings and evaluate performance
        [~,best_param,pred_dev_post] = predpostproc_train(pred_dev,gs_dev(:,best_del),Nw);
        
%         %predict on test with model on train
%         pred_test=predict(gs_test(:,best_del),features_test,model,'-q');
%         
%         %apply post processings and evaluate performance
%         [~,pred_test_post] = predpostproc_test(pred_test,gs_test(:,best_del),best_param);
        
        %shift forward predictions according to the delay
        delay=round(delays(best_del)/Ts);
        if delay>0,
            for sub=1:Nsub,
                pred_dev_post((sub-1)*Nframes+1:sub*Nframes)=...
                    [repmat(pred_dev_post((sub-1)*Nframes+1),delay,1) ; pred_dev_post((sub-1)*Nframes+1:sub*Nframes-delay)];
%                 if m<6 || sub~=Nsub;
%                     %test_7 data is missing on EDA, SCL and SCR (m>5)
%                     pred_test_post((sub-1)*Nframes+1:sub*Nframes)=...
%                         [repmat(pred_test_post((sub-1)*Nframes+1),delay,1) ; pred_test_post((sub-1)*Nframes+1:sub*Nframes-delay)];
%                 end
            end
        end
        
%         %modality -> {EDA, SCL, SCR}
%         if m>5,
%             %insert 0 for missing test_7 predictions
%             pred_test_post=[pred_test_post(1:6*Nframes) ; zeros(Nframes,1) ; pred_test_post(6*Nframes+1:end)];
%             
%             %get test gs from ECG data
%             [~,gs_test] = read_arff(fullfile(AVEC_2016_path,'features_ECG',emo_dim{dim},'stand_test.arff'),Ndel);
%         end
        
        %compute performance with the original gold standard (delay is 0)
        gs_dev=gs_dev(:,1);
%         gs_test=gs_test(:,1);
        CCC_dev_ogs=CCC_calc(pred_dev_post,gs_dev);
%         CCC_test_ogs=CCC_calc(pred_test_post,gs_test);
        
        %save predictions for multimodal fusion
        if m==2 || m==3,
            %save also frames where video data are missing (face not detected)
            %should be 0 but there is the bias in the SVR model
            zero_valup=model.w(end)+eps;
            zero_valdown=model.w(end)-eps;
            frames_video_dev=~(logical(pred_dev>zero_valdown) & logical(pred_dev<zero_valup)); %#ok<NASGU>
%             frames_video_test=~(logical(pred_test>zero_valdown) & logical(pred_test<zero_valup)); %#ok<NASGU>
%             save(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']),'gs_dev','gs_test','pred_dev_post','pred_test_post','CCC_dev_ogs','CCC_test_ogs','best_del','frames_video_dev','frames_video_test');
            save(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']),'gs_dev','pred_dev_post','CCC_dev_ogs','best_del','frames_video_dev');
        else
%             save(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']),'gs_dev','gs_test','pred_dev_post','pred_test_post','CCC_dev_ogs','CCC_test_ogs','best_del');
            save(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']),'gs_dev','pred_dev_post','CCC_dev_ogs','best_del');
        end
    else
        load(fullfile(output_path,['final_results_' emo_dim{dim} '.mat']));
    end
%     fprintf('\t\t-> %s, best delay: %2.1fs, final result: (dev) CCC=%3.3f, (test) CCC=%3.3f\n', emo_dim{dim}, delays(best_del), CCC_dev_ogs, CCC_test_ogs);
    fprintf('\t\t-> %s, best delay: %2.1fs, final result: (dev) CCC=%3.3f\n', emo_dim{dim}, delays(best_del), CCC_dev_ogs);
end
fprintf('\n')