function [CCC_save,pred_post] = predpostproc_test(pred,ref,best_param)

%raw, filter, center, scale, shift
CCC_save=zeros(1,4);

%compute performance on raw
CCC_save(1) = CCC_calc(pred,ref);

%apply filtering
if best_param(1)>0,
    pred=medfilt1(pred,best_param(1));%filter
    CCC_save(2) = CCC_calc(pred,ref);
else
    CCC_save(2) = CCC_save(1);
end

%apply centering
if best_param(2)~=0,
    pred=pred+best_param(2);%center
    CCC_save(3) = CCC_calc(pred,ref);
else
    CCC_save(3) = CCC_save(2);
end

%apply scaling
if best_param(3)~=1,
    pred=pred*best_param(3);%scale
    CCC_save(4) = CCC_calc(pred,ref);
else
    CCC_save(4) = CCC_save(3);
end

pred_post=pred;