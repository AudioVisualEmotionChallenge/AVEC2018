function add_gs(feat_path,emo_dim,Ts,gs_path,delays)

Ndel=length(delays);
Ndim=length(emo_dim);

%generate delayed version of the gold-standard
if isempty(dir(fullfile(gs_path,'gs_delayed.mat'))),
    
    %list of fixed time delays
    delaysTe=round(delays/Ts);
    
    %name of gold standard
    gs_name=cell(Ndim,Ndel);
    for dim=1:Ndim,
        for del=1:Ndel,
            gs_name{dim,del}=[emo_dim{dim} '_' num2str(delays(del)) '_delay'];
        end
    end
    
    %get number of frames
    files=dir(fullfile(gs_path,emo_dim{1},'*.arff'));
    Nf=length(files);
    gold_standard=cell(1,Nf);
    FID=fopen(fullfile(gs_path,emo_dim{1},files(1).name));
    data=textscan(FID,'%s %f %f','Delimiter',{'\n',','},'HeaderLines',9);
    fclose(FID);
    Nframe=size(data{3}',2);
    
    %apply delay to gold standard
    for f=1:Nf,
        gold_standard{f}=zeros(Ndel*Ndim,Nframe);
    end
    for dim=1:Ndim,
        files=dir(fullfile(gs_path,emo_dim{dim},'*.arff'));
        for f=1:Nf,
            FID=fopen(fullfile(gs_path,emo_dim{dim},files(f).name));
            data=textscan(FID,'%s %f %f','Delimiter',{'\n',','},'HeaderLines',9);
            fclose(FID);
            gs=data{3}';
            for del=1:Ndel,
                gold_standard{f}(del+Ndel*(dim-1),:)=[gs(1+delaysTe(del):end) repmat(gs(end),1,delaysTe(del))];
            end
        end
    end
    save(fullfile(gs_path,'gs_delayed.mat'),'gold_standard','gs_name');
else
    data=load(fullfile(gs_path,'gs_delayed.mat'));
    gold_standard=data.gold_standard;
    gs_name=data.gs_name;
    clear 'data';
end

%loop on dimensions
for dim=1:Ndim,
    
    %number of files
    files=[dir(fullfile(feat_path,emo_dim{dim},'dev*.arff')) ; dir(fullfile(feat_path,emo_dim{dim},'train*.arff'))];
%     files=[dir(fullfile(feat_path,emo_dim{dim},'dev*.arff')) ; dir(fullfile(feat_path,emo_dim{dim},'test*.arff')) ; dir(fullfile(feat_path,emo_dim{dim},'train*.arff'))];
    Nf=length(files);
    
    %loop on files
    for f=1:Nf,
        
        if isempty(dir(fullfile(feat_path,emo_dim{dim},['gs_' files(f).name]))),
            %read feature file
            file_path=fullfile(feat_path,emo_dim{dim},files(f).name);
            [features,~,att_name] = read_arff_withatt(file_path,0);
            Nframe=size(features,1);
            Nfeat=size(features,2);
            
            %merge with ratings
            features_withratings=zeros(Nframe,Nfeat+Ndel);
            features_withratings(:,1:Nfeat)=features;
            
            %add the gold standards
            for del=1:Ndel,
                features_withratings(:,Nfeat+del)=gold_standard{f}(del+(dim-1)*Ndel,:);
            end
            
            %save data into arff file
            arffwrite(fullfile(feat_path,emo_dim{dim},['gs_' files(f).name]),['features_' emo_dim{dim} '_gs'],[att_name gs_name(dim,:)],features_withratings');
        end
    end
end