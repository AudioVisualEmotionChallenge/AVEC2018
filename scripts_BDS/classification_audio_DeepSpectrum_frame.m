%feature path
featpath=fullfile(basefeatpath,'LLDs_audio_DeepSpectrum_turns');

% fprintf('\t- loading data')
%concatenate features and labels
featall=cell(1,Np);
featallsp=cell(1,Np);
labelsall=cell(1,Np);
install=cell(1,Np);
parfor p=1:Np,
    Nf=length(labels{p});
    featall{p}=NaN*ones(Nf*300,Natt_DeepSpectrum+1);
    labelsall{p}=NaN*ones(1,Nf*300);
    install{p}=NaN*ones(1,Nf*300);
    cpt=1;
    for f=1:Nf,
        fid=fopen(fullfile(featpath,[parinstname{p}{f} '.csv']));
        data=textscan(fid,['%f' repmat(' %f',1,Natt_DeepSpectrum)],'Delimiter',';','HeaderLines',1,'CollectOutput',1);
        fclose(fid);
        data=data{1};
        Nins=size(data,1);
        featall{p}(cpt:cpt+Nins-1,:)=data;
        labelsall{p}(cpt:cpt+Nins-1)=labels{p}(f);
        install{p}(cpt:cpt+Nins-1)=f;
        cpt=cpt+Nins+1;
    end
    featall{p}=featall{p}(logical(~isnan(featall{p}(:,1))),:);
    labelsall{p}=labelsall{p}(logical(~isnan(labelsall{p})));
    install{p}=install{p}(logical(~isnan(install{p})));
    
    %upsample to majority class training data
    if p==1,
        [featall{p},labelsall{p}]=upsample(featall{p},labelsall{p});
    end
    
    %make sparse format for liblinear
    featallsp{p}=sparse(featall{p}(:,2:end));%remove frametime
end

%classif: best hyper-parameters (C,solverval)
% fprintf(', final predictions')
Cval=0.002;solval=3;

%train model with best setup
options=['-s ' num2str(solval) ' -c ' num2str(Cval) ' -B 1 -q'];
model=train(labelsall{1}',featallsp{1},options);

%predict on dev/test
labels_dev=predict(labelsall{2}',featallsp{2},model,'-q');
% labels_test=predict(labelsall{3}',featallsp{3},model,'-q');

%compute UAR at frame level
%dev
recall=zeros(1,Nclass);
for cl=1:Nclass,
    ind=find(labelsall{2}==cl);
    recall(cl)=length(find(labels_dev(ind)==cl))/length(ind);
end
UAR_devframe=mean(recall);
% %test
% recall=zeros(1,Nclass);
% for cl=1:Nclass,
%     ind=find(labelsall{3}==cl);
%     recall(cl)=length(find(labels_test(ind)==cl))/length(ind);
% end
% UAR_testframe=mean(recall);

%compute UAR at session level
%dev
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
UAR_devsession=mean(recall);
% %test
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
fid=fopen(fullfile(probas_path,'prob_audio_DeepSpectrum_dev'),'wt');
p=2;
Ns=install{p}(end);
for k=1:Ns,
    fprintf(fid,'%g %g %g\n',prob_dev(:,k)');
end
fclose(fid);
% fid=fopen(fullfile(probas_path,'prob_audio_DeepSpectrum_test'),'wt');
% p=3;
% Ns=install{p}(end);
% for k=1:Ns,
%     fprintf(fid,'%g %g %g\n',prob_test(:,k)');
% end
% fclose(fid);

% fprintf('\n\t frame-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devframe,100*UAR_testframe)
% fprintf('\t session-dev: %3.2f%%, test: %3.2f%%\n',100*UAR_devsession,100*UAR_testsession)
fprintf('\t session-dev: %3.2f%%\n',100*UAR_devsession)