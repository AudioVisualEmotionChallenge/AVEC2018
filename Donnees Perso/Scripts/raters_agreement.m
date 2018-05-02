function [RMSE,CC,CCC,ICC,alpha] = raters_agreement(ratings)

%number of raters
Nr=size(ratings,1);

%Cnk pairs of raters
rater_cnk=combnk(1:Nr,2);
Ncnk=size(rater_cnk,1);

%compute agreement with the different metrics
RMSE=zeros(1,Ncnk);
CC=zeros(1,Ncnk);
CCC=zeros(1,Ncnk);
for k=1:Ncnk,
    [RMSE(k),CC(k),CCC(k)] = raters_statistics(ratings(rater_cnk(k,1),:),ratings(rater_cnk(k,2),:));
end

%ICC
ICC=ICC_shrout(3,'k',ratings');

%alpha
[alpha,~,~]=cronbach(ratings');

RMSE=mean(RMSE);
CC=mean(CC);
CCC=mean(CCC);