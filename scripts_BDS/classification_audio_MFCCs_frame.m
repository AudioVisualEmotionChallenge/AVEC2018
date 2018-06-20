%feature path
featpath=fullfile(basefeatpath,'LLDs_audio_opensmile_MFCCs_turns');

%keep one instance every 100
keepinst=100;

% fprintf('\t- loading data')
%concatenate features and labels
featall=cell(1,Np);
labelsall=cell(1,Np);
install=cell(1,Np);
parfor p=1:Np,
    Nf=length(labels{p});
    featall{p}=NaN*ones(Nf*2e4,Natt_MFCCs-1);
    labelsall{p}=NaN*ones(1,Nf*2e4);
    install{p}=NaN*ones(1,Nf*2e4);
    cpt=1;
    for f=1:Nf,
        %load features
        fid=fopen(fullfile(featpath,[parinstname{p}{f} '.csv']));
        data=textscan(fid,['%s' repmat(' %f',1,Natt_MFCCs-1)],'Delimiter',';','HeaderLines',1);
        fclose(fid);
        data=data(2:end);
        data=[data{:}];
        Nins=size(data,1);
        indins=1:keepinst:Nins;
        Nins=length(indins);
        %concatenate them
        featall{p}(cpt:cpt+Nins-1,:)=data(indins,:);
        labelsall{p}(cpt:cpt+Nins-1)=labels{p}(f);
        install{p}(cpt:cpt+Nins-1)=f;
        cpt=cpt+Nins+1;
    end
    featall{p}=featall{p}(logical(~isnan(featall{p}(:,1))),:);
    labelsall{p}=labelsall{p}(logical(~isnan(labelsall{p})));
    install{p}=install{p}(logical(~isnan(install{p})));
end
%training set
p=1;
meanval=mean(featall{p}(:,2:end));%1 is frametime
stdval=std(featall{p}(:,2:end));
featallsp=cell(1,Np);
for p=1:Np,
    %standardise features
    Nins=size(featall{p},1);
    featall{p}(:,2:end)=(featall{p}(:,2:end)-repmat(meanval,Nins,1))./repmat(stdval,Nins,1);
    
    %upsample to majority class training data
    if p==1,
        [featall{p},labelsall{p}]=upsample(featall{p},labelsall{p});
    end
    
    %make sparse format for liblinear
    featallsp{p}=sparse(featall{p}(:,2:end));%remove frametime
end
    
%classif: optimisation of hyper-parameters (C,solverval)
% fprintf(', model optimisation')
UAR_frame=zeros(Nsol,Nc);
UAR_session=zeros(Nsol,Nc);
for sol=1:Nsol,
     parfor c=1:Nc,
         %train model
         options=['-s ' num2str(solver_val(sol)) ' -c ' num2str(C(c)) ' -B 1 -q'];
         model=train(labelsall{1}',featallsp{1},options);
         
         %predict with model on dev
         labels_dev=predict(labelsall{2}',featallsp{2},model,'-q');
         
         %compute UAR at frame level
         recall=zeros(1,Nclass);
         for cl=1:Nclass,
             ind=find(labelsall{2}==cl);
             recall(cl)=length(find(labels_dev(ind)==cl))/length(ind);
         end
         UAR_frame(sol,c)=mean(recall);
         
         %compute UAR at session level
         Ns=install{2}(end);
         final_decision=zeros(1,Ns);
         for s=1:Ns,
             inds=find(install{2}==s);
             classcount=zeros(1,Nclass);
             for cl=1:Nclass,
                 classcount(cl)=length(find(labels_dev(inds)==cl));
             end
             [~,final_decision(s)]=max(classcount);
         end
         recall=zeros(1,Nclass);
         for cl=1:Nclass,
             ind=find(labels{2}==cl);
             recall(cl)=length(find(final_decision(ind)==cl))/length(ind);
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
UAR_devframe=UAR_frame(indbest_sol,indbest_c);

%train model with best setup
options=['-s ' num2str(solver_val(indbest_sol)) ' -c ' num2str(C(indbest_c)) ' -B 1 -q'];
model=train(labelsall{1}',featallsp{1},options);

%predict on dev and test
labels_dev=predict(labelsall{2}',featallsp{2},model,'-q');
% labels_test=predict(labelsall{3}',featallsp{3},model,'-q');

% %compute UAR at frame level
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labelsall{3}==cl);
%     recall(cl)=length(find(labels_test(ind)==cl))/length(ind);
% end
% UAR_testframe=mean(recall);
% 
% %compute UAR at session level
% Ns=install{3}(end);
% final_decision=zeros(1,Ns);
% for s=1:Ns,
%     inds=find(install{3}==s);
%     classcount=zeros(1,Nclass);
%     for cl=1:Nclass,
%         classcount(cl)=length(find(labels_test(inds)==cl));
%     end
%     [~,final_decision(s)]=max(classcount);
% end
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labels{3}==cl);
%     recall(cl)=length(find(final_decision(ind)==cl))/length(ind);
% end
% UAR_testsession=mean(recall);

%generate a posteriori probablities
p=2;
Ns=install{p}(end);
prob_dev=zeros(Nclass,Ns);
for s=1:Ns,
    inds=find(install{p}==s);
    Nins=length(inds);
    for cl=1:Nclass,
        prob_dev(cl,s)=length(find(labels_dev(inds)==cl))/Nins;
    end
end
% p=3;
% Ns=install{p}(end);
% prob_test=zeros(Nclass,Ns);
% for s=1:Ns,
%     inds=find(install{p}==s);
%     Nins=length(inds);
%     for cl=1:Nclass,
%         prob_test(cl,s)=length(find(labels_test(inds)==cl))/Nins;
%     end
% end

%save prob in files
fid=fopen(fullfile(probas_path,'prob_audio_mfcc_dev'),'wt');
p=2;
Ns=install{p}(end);
for k=1:Ns,
    fprintf(fid,'%g %g %g\n',prob_dev(:,k)');
end
fclose(fid);
% fid=fopen(fullfile(probas_path,'prob_audio_mfcc_test'),'wt');
% p=3;
% Ns=install{p}(end);
% for k=1:Ns,
%     fprintf(fid,'%g %g %g\n',prob_test(:,k)');
% end
% fclose(fid);


% fprintf('\n\t- frame-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devframe,100*UAR_testframe)
% fprintf('\t- session-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devsession,100*UAR_testsession)
fprintf('\t- session-dev: %3.2f%%\n',100*UAR_devsession)