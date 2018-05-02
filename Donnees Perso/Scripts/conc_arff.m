function conc_arff(feat_path,emo_dim)

%list of partitions
Np=2;
partitions=cell(1,Np);
partitions{1}='train';
partitions{2}='dev';
% partitions{3}='test';

Ndim=length(emo_dim);

%loop on dimensions
for dim=1:Ndim,
    
    %loop on partitions
    for p=1:Np,
        
        if isempty(dir(fullfile(feat_path,emo_dim{dim},['conc_' partitions{p} '.arff']))),
            
            %list files
            files=dir(fullfile(feat_path,emo_dim{dim},['gs_' partitions{p} '*.arff']));
            Nf=length(files);
            
            %concatenate data
            Feats_val=cell(1,Nf);
            for f=1:Nf,
                if f==1,
                    [Feats_val{f},~,Feats_name] = read_arff_withatt(fullfile(feat_path,emo_dim{dim},files(f).name),0);
                else
                    [Feats_val{f},~] = read_arff(fullfile(feat_path,emo_dim{dim},files(f).name),0);
                end
                Feats_val{f}=Feats_val{f}';
            end
            
            %write data
            arffwrite(fullfile(feat_path,emo_dim{dim},['conc_' partitions{p} '.arff']),['features_' emo_dim{dim} '_gs_conc'],Feats_name,[Feats_val{:}]);
        end
    end
end