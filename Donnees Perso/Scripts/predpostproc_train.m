function [CCC_save,best_param,pred_post] = predpostproc_train(pred,ref,Nw)

%raw, filter, center, scale
CCC_save=zeros(1,4);
%wmedian, bias, scale
best_param=zeros(1,3);

%compute performance on raw
CCC_save(1) = CCC_calc(pred,ref);
best_CCC=CCC_save(1);

%filter by dichotomy (save a lot of time...)
perc_impr=2;

new_val=zeros(1,4);
new_val(1)=CCC_save(1);
pred_filt_save=cell(1,3);
for k=1:3,
    pred_filt_save{k}=medfilt1(pred,round(k*Nw/3));
    new_val(k+1)=CCC_calc(pred_filt_save{k},ref);
end

[val,indw]=sort(new_val,'descend');
if indw(1)~=1 && 100*(val(1)-new_val(1))/new_val(1)>perc_impr,
    %filtering useful
    pred_filt_save=pred_filt_save{indw(1)-1};
    
    %perform second round of dichotomy
    indw=round((indw(1:2)-1)*Nw/3);
    new_indw=[indw(1) round(mean(indw)) indw(2)];
    pred_filt=medfilt1(pred,new_indw(2));
    new_val=[val(1) CCC_calc(pred_filt,ref) val(2)];
    
    %continue dichotomy if still improvement
    if 100*(new_val(2)-max(new_val([1 3])))/max(new_val([1 3]))>perc_impr,
        eot=1;
        while eot,
            [val,indw]=sort(new_val,'descend');
            new_indw=[new_indw(indw(1)) round(mean(new_indw(indw(1:2)))) new_indw(indw(2))];
            pred_filt=medfilt1(pred,new_indw(2));
            new_val=[val(1) CCC_calc(pred_filt,ref) val(2)];
            if 100*(new_val(2)-max(new_val([1 3])))/max(new_val([1 3]))>perc_impr,
                %save prediction in case next step round will perfrom worse
                pred_filt_save=pred_filt;
            else
                %save prediction if there is yet improvement
                if 100*(new_val(2)-max(new_val([1 3])))/max(new_val([1 3]))>0,
                    best_param(1)=new_indw(2);
                    pred=pred_filt;
                    best_CCC=new_val(2);
                else
                    best_param(1)=new_indw(1);
                    pred=pred_filt_save;
                    best_CCC=val(1);
                end
                eot=0;
            end
        end
    else
        if 100*(new_val(2)-max(new_val([1 3])))/max(new_val([1 3]))>0,
            best_param(1)=new_indw(2);
            pred=pred_filt;
            best_CCC=new_val(2);
        else
            best_param(1)=indw(1);
            pred=pred_filt_save;
            best_CCC=val(1);
        end
    end
else
    if 100*(val(1)-new_val(1))/new_val(1)>perc_impr,
        %filtering bring improvement smaller than perc_impr
        best_param(1)=(indw(1)-1)*Nw/3;
        pred=pred_filt_save{indw(1)-1};
        best_CCC=val(1);
    else
        %filtering not useful
        best_param(1)=0;
    end
end
CCC_save(2)=best_CCC;

%center prediction
mean_ref=mean(ref);
mean_pred=mean(pred);
bias=mean_ref-mean_pred;
pred_center=pred+bias;%center

CCC_tmp=CCC_calc(pred_center,ref);
%save configuration if improvement
if CCC_tmp>best_CCC,
    best_CCC=CCC_tmp;
    best_param(2)=bias;
    pred=pred_center;
else
    best_param(2)=0;
end
CCC_save(3)=best_CCC;

%scale prediction
std_ref=std(ref);
std_pred=std(pred);
scale=std_ref/std_pred;
pred_scale=pred*scale;%scale

%save configuration if improvement
CCC_tmp=CCC_calc(pred_scale,ref);
if CCC_tmp>best_CCC,
    best_CCC=CCC_tmp;
    best_param(3)=scale;
    pred=pred_scale;
else
    best_param(3)=1;
end
CCC_save(4)=best_CCC;

pred_post=pred;