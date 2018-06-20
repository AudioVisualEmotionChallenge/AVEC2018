%read values
prob_audio=cell(Np,Nar);
prob_video=cell(Np,Nvr);
for r=1:Nar,
    for p=2:Np,
        fid=fopen(fullfile(probas_path,[audio_rep{r} '_' part{p}]));
        data=textscan(fid,'%f %f %f','Delimiter',' ','CollectOutput',1);
        fclose(fid);
        prob_audio{p,r}=data{1};
        if r<=Nvr,
            fid=fopen(fullfile(probas_path,[video_rep{r} '_' part{p}]));
            data=textscan(fid,'%f %f %f','Delimiter',' ','CollectOutput',1);
            fclose(fid);
            prob_video{p,r}=data{1};
        end
    end
end

%check performance on audio and video for all representations
UAR_audio=zeros(Np,Nar);UAR_video=zeros(Np,Nvr);
for ar=1:Nar,
    for p=2:Np,
        [~,labels_fus]=max(prob_audio{p,ar},[],2);
        recall=zeros(1,Nclass);
        for cl=1:Nclass,
            ind=find(labels{p}==cl);
            recall(cl)=length(find(labels_fus(ind)==cl))/length(ind);
        end
        UAR_audio(p,ar)=mean(recall);
        if ar<=Nvr,
            [~,labels_fus]=max(prob_video{p,ar},[],2);
            recall=zeros(1,Nclass);
            for cl=1:Nclass,
                ind=find(labels{p}==cl);
                recall(cl)=length(find(labels_fus(ind)==cl))/length(ind);
            end
            UAR_video(p,ar)=mean(recall);
        end
    end
end

%fuse each of the best two audio representations with the best video representation
fprintf('\n* Audiovisual: Fusion of a posteriori probas - eGeMAPS and FAUs\n')
featall=cell(1,Np);
for p=1:Np
    featall{p}=[prob_audio{p,2} prob_video{p,1}]; 
end
p=2;
meanval=nanmean(featall{p});
stdval=nanstd(featall{p});
featallsp=cell(1,Np);
for p=2:Np,
    %standardise features
    Nins=size(featall{p},1);
    featall{p}=(featall{p}-repmat(meanval,Nins,1))./repmat(stdval,Nins,1);
    
    %upsample to majority class training data
    if p==2,
        [featall{p},labelsup]=upsample(featall{p},labels{p});
    end

    %make sparse format for liblinear
    featallsp{p}=sparse(featall{p});
end

%classif: optimisation of hyper-parameters (C,solverval)
UAR_session=zeros(Nsol,Nc);
p=2;
for sol=1:Nsol,
    for c=1:Nc,
        %train model
        options=['-s ' num2str(solver_val(sol)) ' -c ' num2str(C(c)) ' -B 1 -q'];
        model=train(labelsup',featallsp{p},options);
        
        %predict with model on dev
        labels_dev=predict(labelsup',featallsp{p},model,'-q');
        
        %compute UAR at session level
        recall=zeros(1,Nclass);
        for cl=1:Nclass,
            ind=find(labelsup==cl);
            recall(cl)=length(find(labels_dev(ind)==cl))/length(ind);
        end
        UAR_session(sol,c)=mean(recall);
    end
end

%we keep the lower complexity between best solvers in case of a draw
[val,ind]=max(UAR_session);
indbest_sol=ind;
[UAR_devsession,ind]=max(val);
indbest_sol=indbest_sol(ind);
indbest_c=ind;

%train model with best setup
options=['-s ' num2str(solver_val(indbest_sol)) ' -c ' num2str(C(indbest_c)) ' -B 1 -q'];
model=train(labelsup',featallsp{p},options);

%predict on dev and test
% labels_dev=predict(labelsup',featallsp{p},model,'-q');
% labels_test=predict(labels{p+1}',featallsp{p+1},model,'-q');

% %compute UAR at session level
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labels{p+1}==cl);
%     recall(cl)=length(find(labels_test(ind)==cl))/length(ind);
% end
% UAR_testsession=mean(recall);

fprintf('\t- session-dev: %3.2f%%\n',100*UAR_devsession)


%fuse each of the best two audio representations with the best video representation
fprintf('\n* Audiovisual: Fusion of a posteriori probas - DeepSpectrum and FAUs\n')
featall=cell(1,Np);
for p=1:Np
    featall{p}=[prob_audio{p,4} prob_video{p,1}]; 
end
p=2;
meanval=nanmean(featall{p});
stdval=nanstd(featall{p});
featallsp=cell(1,Np);
for p=2:Np,
    %standardise features
    Nins=size(featall{p},1);
    featall{p}=(featall{p}-repmat(meanval,Nins,1))./repmat(stdval,Nins,1);
    
    %upsample to majority class training data
    if p==2,
        [featall{p},labelsup]=upsample(featall{p},labels{p});
    end

    %make sparse format for liblinear
    featallsp{p}=sparse(featall{p});
end

%classif: optimisation of hyper-parameters (C,solverval)
UAR_session=zeros(Nsol,Nc);
p=2;
for sol=1:Nsol,
    for c=1:Nc,
        %train model
        options=['-s ' num2str(solver_val(sol)) ' -c ' num2str(C(c)) ' -B 1 -q'];
        model=train(labelsup',featallsp{p},options);
        
        %predict with model on dev
        labels_dev=predict(labelsup',featallsp{p},model,'-q');
        
        %compute UAR at session level
        recall=zeros(1,Nclass);
        for cl=1:Nclass,
            ind=find(labelsup==cl);
            recall(cl)=length(find(labels_dev(ind)==cl))/length(ind);
        end
        UAR_session(sol,c)=mean(recall);
    end
end

%we keep the lower complexity between best solvers in case of a draw
[val,ind]=max(UAR_session);
indbest_sol=ind;
[UAR_devsession,ind]=max(val);
indbest_sol=indbest_sol(ind);
indbest_c=ind;

%train model with best setup
options=['-s ' num2str(solver_val(indbest_sol)) ' -c ' num2str(C(indbest_c)) ' -B 1 -q'];
model=train(labelsup',featallsp{p},options);

%predict on dev and test
labels_dev=predict(labelsup',featallsp{p},model,'-q');
% labels_test=predict(labels{p+1}',featallsp{p+1},model,'-q');

% %compute UAR at session level
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labels{p+1}==cl);
%     recall(cl)=length(find(labels_test(ind)==cl))/length(ind);
% end
% UAR_testsession=mean(recall);

% fprintf('\t- session-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devsession,100*UAR_testsession)
fprintf('\t- session-dev: %3.2f%%\n',100*UAR_devsession)