function [features,classes_val,att_name] = read_arff_withatt(arff_path,Ncl)

%get number of attributes
eof=0;att_cpt=0;
FID=fopen(arff_path);
if FID>0,
    att_name=cell(1,99999);
    while ~eof,
        data=textscan(FID,'%s %s %s',1,'Delimiter',' ');
        if strcmp(data{1},'@attribute'),
            att_cpt=att_cpt+1;
            att_name{att_cpt}=data{2};
        end
        if strcmp(data{1},'@data'),
            eof=1;
        end
    end
    Natt=att_cpt-Ncl;
    att_name=[att_name{1:Natt}];
    fclose(FID);
    
    %get headerlines
    FID=fopen(arff_path);
    data=textscan(FID,'%s','Delimiter','\n');
    fclose(FID);
    data=data{1};
    Nlines=size(data,1);
    for l=1:Nlines,
        if strcmp(data{l},'@data'),
            headerlines=l+1;
            break
        end
    end
    
    %get values for features and class(es)
    FID=fopen(arff_path);
    data=textscan(FID,['%f' repmat(' %f',1,Natt-1) repmat(' %f',1,Ncl)],'Delimiter',',','HeaderLines',headerlines,'TreatAsEmpty','?');
    fclose(FID);
    
    features=[data{1:Natt}];
    if Ncl>0,
        classes_val=[data{Natt+1:end}];
    else
        classes_val=[];
    end
else
    features=NaN;
    classes_val=NaN;
    disp(['Error while opening ' arff_path])
end