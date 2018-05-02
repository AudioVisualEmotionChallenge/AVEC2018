function CCC = CCC_calc(pred,ref)

pred_mean=nanmean(pred);
ref_mean=nanmean(ref);

pred_var=nanvar(pred);
ref_var=nanvar(ref);

covariance=nanmean((pred-pred_mean).*(ref-ref_mean));

CCC=(2*covariance)/(pred_var+ref_var+(pred_mean-ref_mean)^2);