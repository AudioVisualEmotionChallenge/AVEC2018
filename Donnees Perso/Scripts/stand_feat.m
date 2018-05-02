function stand_feat(feat_path,emo_dim,stand_app)

Np=2;
partitions=cell(1,Np);
partitions{1}='dev';
partitions{2}='train';
% partitions{3}='test';
Nframes=7501;
Ndim=length(emo_dim);

for dim=1:Ndim,
    
    if stand_app(dim)==1,
        %online
        
        if isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_train.arff'))) || isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'))),
%         if isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_train.arff'))) || isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'))) || isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_test.arff'))),
            
            %compute mean and std from train data
            [Feats,~,Feats_name] = read_arff_withatt(fullfile(feat_path,emo_dim{dim},'conc_train.arff'),0);
            meanval=nanmean(Feats);
            stdval=nanstd(Feats);
            
            %list attributes which include features and not annotation data
            N=size(Feats,2);
            for i=1:N,
                if length(Feats_name{i})>6 && strcmp(Feats_name{i}(1:7),emo_dim{dim}),
                    break
                end
            end
            indfeat=1:i-1;
            meanval=meanval(indfeat);
            stdval=stdval(indfeat);
            
            %standardise train
            if isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_train.arff')))
                N=size(Feats,1);
                Feats(:,indfeat)=(Feats(:,indfeat)-repmat(meanval,N,1))./repmat(stdval,N,1);
                arffwrite(fullfile(feat_path,emo_dim{dim},'stand_train.arff'),'standardised_features',Feats_name,Feats');
            end
            
            %apply it to dev data
            if isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'))),
                [Feats,~] = read_arff(fullfile(feat_path,emo_dim{dim},'conc_dev.arff'),0);
                N=size(Feats,1);
                Feats(:,indfeat)=(Feats(:,indfeat)-repmat(meanval,N,1))./repmat(stdval,N,1);
                arffwrite(fullfile(feat_path,emo_dim{dim},'stand_dev.arff'),'standardised_features',Feats_name,Feats');
            end
            
%             %apply it to test data
%             if isempty(dir(fullfile(feat_path,emo_dim{dim},'stand_test.arff'))),
%                 [Feats,~] = read_arff(fullfile(feat_path,emo_dim{dim},'conc_test.arff'),0);
%                 N=size(Feats,1);
%                 Feats(:,indfeat)=(Feats(:,indfeat)-repmat(meanval,N,1))./repmat(stdval,N,1);
%                 arffwrite(fullfile(feat_path,emo_dim{dim},'stand_test.arff'),'standardised_features',Feats_name,Feats');
%             end
        end
    else
        %per subject
        
        %loop on partitions
        for p=1:Np,
            if isempty(dir(fullfile(feat_path,emo_dim{dim},['stand_' partitions{p} '.arff']))),
                [Feats,~,Feats_name] = read_arff_withatt(fullfile(feat_path,emo_dim{dim},['conc_' partitions{p} '.arff']),0);
                
                %list attributes which include features and not annotation data
                N=size(Feats,2);
                for i=1:N,
                    if length(Feats_name{i})>6 && strcmp(Feats_name{i}(1:7),emo_dim{dim}),
                        break
                    end
                end
                indfeat=1:i-1;
                
                %number of files in this partition
                Nfilpart=length(dir(fullfile(feat_path,emo_dim{dim},[partitions{p} '*.arff'])));
                
                %standardise data from each subject
                for f=1:Nfilpart,
                    indf=1+(f-1)*Nframes:f*Nframes;
                    meanval=nanmean(Feats(indf,indfeat));
                    stdval=nanstd(Feats(indf,indfeat));
                    Feats(indf,indfeat)=(Feats(indf,indfeat)-repmat(meanval,Nframes,1))./repmat(stdval,Nframes,1);
                end
                
                %write data
                arffwrite(fullfile(feat_path,emo_dim{dim},['stand_' partitions{p} '.arff']),'standardised_features',Feats_name,Feats');
            end
        end
    end
end