function arffwrite(arffpath,relation,Feats_name,Feats_val,Inst_name)

%Ninst / Nfeats
Ninst=size(Feats_val,2);
Nfeats=size(Feats_val,1);

%write data into ARFF file
fileID=fopen(arffpath,'wt');

%write header
fprintf(fileID,['@relation ' relation '\n\n']);

%write attributes
%first -> string, last -> class
if nargin>4,
    fprintf(fileID,'@attribute Instance_name string\n');
end
for i=1:Nfeats,
    fprintf(fileID,['@attribute ' Feats_name{i} ' numeric\n']);
end
fprintf(fileID,'\n\n@data\n\n');

%write features val
for i=1:Ninst,
    %get features value for instance i
    data=[Feats_val(:,i)' 0];
    %-> double into string
    data=num2str(data);
    %replace NaN in ? for weka
    data=strrep(data,'NaN','?');
    %transform space in comma
    data=strrep(data,' ',',');
    %suppress extra commas
    indind=ones(1,length(data));
    ind=strfind(data,',');
    indind(ind)=0;
    ind2=find(diff(ind)>1);
    indind(ind(ind2))=1; %#ok<*FNDSB>
    data=data(logical(indind));
    data=data(1:end-1);
    %add instance name and class
    if nargin>4,
        data=[Inst_name{i} ',' data '\n']; %#ok<*AGROW>
    else
        data=[data '\n']; %#ok<*AGROW>
    end
    
    %write data into arff file
    fprintf(fileID,data);
end
fclose(fileID);
