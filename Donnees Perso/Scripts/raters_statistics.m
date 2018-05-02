function [RMSE,CC,CCC] = raters_statistics(r1,r2)

%MSE
MSE=nanmean((r1-r2).^2);

%RMSE
RMSE=sqrt(MSE);

%CC
r1_mean=nanmean(r1);
r2_mean=nanmean(r2);
r1_std=nanstd(r1);
r2_std=nanstd(r2);
covariance=nanmean((r1-r1_mean).*(r2-r2_mean));
CC=covariance/(r1_std*r2_std);

%CCC
r1_var=r1_std^2;r2_var=r2_std^2;
CCC=(2*covariance)/(r1_var+r2_var+(r1_mean-r2_mean)^2);