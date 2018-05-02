function liblinear_pred(feat_path,output_path,emo_dim,delays,runpar)

%commands for libsvm
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1];
Nc=length(C);
solver_val=12;%L2L2_dual

Ndel=length(delays);
Ndim=length(emo_dim);

%early stopping in optimisation of gold standard delay
earlystop=3;

%parameters for post-processing
Nw=500;

%perform model training and optimisation
for dim=1:Ndim,
    if isempty(dir(fullfile(output_path,['dev_all_results_' emo_dim{dim} '.mat']))),
        
        %read train and valid data
        [features_train,gs_train] = read_arff(fullfile(feat_path,emo_dim{dim},'stand_train.arff'),Ndel);
        [features_dev,gs_dev] = read_arff(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'),Ndel);
        
        %remove frametime
        features_train=features_train(:,2:end);
        features_dev=features_dev(:,2:end);
        
        %force to zero NaN values
        features_train(logical(isnan(features_train)))=0;
        features_dev(logical(isnan(features_dev)))=0;
        
        %sparse format
        features_train=sparse(features_train);
        features_dev=sparse(features_dev);
        
        CCC_valid=zeros(Nc,Ndel);
        
        %loop on delays
        for del=1:Ndel,
            
            %gold standards
            gs_train_tmp=gs_train(:,del);
            gs_dev_tmp=gs_dev(:,del);
            
            %loop on complexity val
            if runpar,
                parfor c=1:Nc,
                    
                    %train model
                    options=['-s ' num2str(solver_val) ' -c ' num2str(C(c)) ' -B 1 -q'];
                    model=train(gs_train_tmp,features_train,options);
                    
                    %predict with model on dev
                    labels=predict(gs_dev_tmp,features_dev,model,'-q');
                    
                    %learn the post processings and evaluate performance
                    [CCC,~,~] = predpostproc_train(labels,gs_dev_tmp,Nw);
                    CCC_valid(c,del)=CCC(end);
                    
                end
            else
                for c=1:Nc,
                    
                    %train model
                    options=['-s ' num2str(solver_val) ' -c ' num2str(C(c)) ' -B 1 -q'];
                    model=train(gs_train_tmp,features_train,options);
                    
                    %predict with model on dev
                    labels=predict(gs_dev_tmp,features_dev,model,'-q');
                    
                    %learn the post processings and evaluate performance
                    [CCC,~,~] = predpostproc_train(labels,gs_dev_tmp,Nw);
                    CCC_valid(c,del)=CCC(end);
                    
                end
            end
            
            %early stopping
            if del>1,
                max_CCC_tmp=max(max(CCC_valid(:,1:del-1)));
                if max(CCC_valid(:,del))<max_CCC_tmp
                    it_no_imp=it_no_imp+1;
                else
                    it_no_imp=0;
                end
            else
                it_no_imp=0;
            end
            fprintf('\t\t-> %s, delay=%2.1fs, CCC=%3.3f\n', emo_dim{dim}, delays(del), max(CCC_valid(:,del)))
            if it_no_imp==earlystop,
                fprintf('\t\t-> early stopping, no improvement in the last %d iterations\n\n',earlystop);
                break
            end
        end
        
        %save optimisation results
        save(fullfile(output_path,['dev_all_results_' emo_dim{dim} '.mat']),'CCC_valid');
    end
end