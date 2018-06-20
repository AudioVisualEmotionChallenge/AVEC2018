function [featup,labelup] = upsample(feat,label)

%#classes
class=unique(label);Ncl=length(class);

%#instances per class
class_inst=cell(1,Ncl);Ninst_class=zeros(1,Ncl);
for c=1:Ncl,
    class_inst{c}=find(label==class(c));
    Ninst_class(c)=length(class_inst{c});
end

%get upsampling factor and # of remaining instances for each class
max_Ninst_class=max(Ninst_class);
factorup=zeros(1,Ncl);
remainup=zeros(1,Ncl);
for c=1:Ncl,
    factorup(c)=floor(max_Ninst_class/Ninst_class(c));
    remainup(c)=max_Ninst_class-(Ninst_class(c)*factorup(c));
end

%do upsampling
featup=cell(1,Ncl);
labelup=cell(1,Ncl);
for c=1:Ncl,
    %random/fixed selection of remaining instances
%     ind_rem=randperm(Ninst_class(c));
    ind_rem=1:remainup(c);
    ind_rem=ind_rem(1:remainup(c));
    featup{c}=[repmat(feat(class_inst{c},:),factorup(c),1);feat(class_inst{c}(ind_rem),:)]';
    labelup{c}=[repmat(label(class_inst{c}),1,factorup(c)) label(class_inst{c}(ind_rem))];
end
featup=[featup{:}]';
labelup=[labelup{:}];