%path of features
featpath=fullfile(basefeatpath,'LLDs_video_openFace_AUs');

%concatenate features and labels
% fprintf('\t- loading data')
featall=cell(1,Np);
parfor p=1:Np,
    Nf=length(labels{p});
    featall{p}=zeros(Nf,(Natt_FAUs-1-5)*3-1);%remove last 5 features as all NaNs
    cpt=1;
    for f=1:Nf,
        %load features
        fid=fopen(fullfile(featpath,[parinstname{p}{f} '.csv']));
        data=textscan(fid,['%f' repmat(' %f',1,Natt_FAUs-1)],'Delimiter',';','HeaderLines',1);
        fclose(fid);
        data=data([1,3:end-5]);
        data=[data{:}];
        
        %compute stats (mean, std, relative position of max)
        [~,ind]=max(data);
        Nins=size(data,1);
        max_relpo=ind/Nins;
        featall{p}(f,:)=[nanmean(data) nanstd(data) max_relpo(2:end)];
    end
end

meanval=nanmean(featall{1});
stdval=nanstd(featall{1});
featallsp=cell(1,Np);
for p=1:Np,
    %standardise features
    Nins=size(featall{p},1);
    featall{p}=(featall{p}-repmat(meanval,Nins,1))./repmat(stdval,Nins,1);
    
    %upsample to majority class training data
    if p==1,
        [featall{p},labelsup]=upsample(featall{p},labels{p});
        labelsup=labelsup';
    end
    
    %make sparse format for liblinear
    featallsp{p}=sparse(featall{p});
end

%classif: optimisation of hyper-parameters (C,solverval)
% fprintf(', model optimisation')
UAR_session=zeros(2,Nc);
solversval=6:7;%only logistic regression to get probas
for sol=1:2,
    for c=1:Nc,
        %train model
        options=['-s ' num2str(solversval(sol)) ' -c ' num2str(C(c)) ' -B 1 -q'];
        model=train(labelsup,featallsp{1},options);
        
        %predict with model on dev
        labels_dev=predict(labels{2}',featallsp{2},model,'-q');
        
        %compute UAR at session level
        recall=zeros(1,Nclass);
        for cl=1:Nclass,
            ind=find(labels{2}==cl);
            recall(cl)=length(find(labels_dev(ind)==cl))/length(ind);
        end
        UAR_session(sol,c)=mean(recall);
    end
end

%we keep the lower complexity between best solvers in case of a draw
% fprintf(', final predictions')
[val,ind]=max(UAR_session);
indbest_sol=ind;
[UAR_devsession,ind]=max(val);
indbest_sol=indbest_sol(ind);
indbest_c=ind;

%train model with best setup
options=['-s ' num2str(solversval(indbest_sol)) ' -c ' num2str(C(indbest_c)) ' -B 1 -q'];
model=train(labelsup,featallsp{1},options);

%predict on dev and test
[labels_dev,~,decision_dev]=predict(labels{2}',featallsp{2},model,' -b -q');
% [labels_test,~,decision_test]=predict(labels{3}',featallsp{3},model,' -b -q');

% %compute UAR at session level
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labels{3}==cl);
%     recall(cl)=length(find(labels_test(ind)==cl))/length(ind);
% end
% UAR_testsession=mean(recall);

%compute a posteriori probas from decisions
minval=min(min(decision_dev));
prob_dev=decision_dev-minval;
prob_dev=prob_dev./repmat(sum(prob_dev,2),1,3);

% minval=min(min(decision_test));
% prob_test=decision_test-minval;
% prob_test=prob_test./repmat(sum(prob_test,2),1,3);

%save probas in files
fid=fopen(fullfile(probas_path,'prob_video_FAUs_dev'),'wt');
p=2;
Ns=install{p}(end);
for k=1:Ns,
    fprintf(fid,'%g %g %g\n',prob_dev(k,:));
end
fclose(fid);
% fid=fopen(fullfile(probas_path,'prob_video_FAUs_test'),'wt');
% p=3;
% Ns=install{p}(end);
% for k=1:Ns,
%     fprintf(fid,'%g %g %g\n',prob_test(k,:));
% end
% fclose(fid);

% fprintf('\t- session-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devsession,100*UAR_testsession)
fprintf('\t- session-dev: %3.2f%%\n',100*UAR_devsession)