%This is the script to reproduce the gold standard from individual ratings
%on AVEC 2016 MASC. 

clear all, %#ok<CLSCR>
clc

%% path to data

%path containing features and gold standard
AVEC_2016_path='/home/adrien/Bureau/TER';
gs_path=fullfile(AVEC_2016_path,'ratings_gold_standard');
ir_path=fullfile(AVEC_2016_path,'ratings_individual');


%% declaration of constants

%emotional dimensions
Ndim=2;
emo_dim=cell(1,Ndim);
emo_dim{1}='arousal';
emo_dim{2}='valence';

%number of raters
Nr=6;

%number of frames per rating
Nframe=7501;

%number of files
Nf=18;

%frametme in seconds
frametime=0:0.04:300;

%% get all ratings on train and dev partitions

fprintf('-> Reading individual ratings...\n');

all_ratings=cell(Ndim,Nf);
for d=1:Ndim,
    files=dir(fullfile(ir_path,emo_dim{d},'*.csv'));
    for f=1:Nf,
        FID=fopen(fullfile(ir_path,emo_dim{d},files(f).name));
        data=textscan(FID,['%f' repmat(' %f',1,Nr)],'Delimiter',';','HeaderLines',1);
        fclose(FID);
        all_ratings{d,f}=[data{2:end}]';    
    end
end

%% compute inter-rater agreement on raw
%
%please note that the values reported here slightly differ from Table 1, as
%statistics given in this table include the test files.
%

fprintf('-> Compute inter-rater agreement on raw...\n');

%Cnk pairs of raters
rater_cnk=combnk(1:Nr,2);
Ncnk=size(rater_cnk,1);

%define where each rater is in the Cnk matrix
rater_appearance=zeros(Nr-1,Nr);
for r=1:Nr,
    rater_appearance(:,r)=[find(rater_cnk(:,1)==r) ; find(rater_cnk(:,2)==r)];
end

% compute agreement
RMSE_raw=zeros(1,Ndim);
CC_raw=zeros(1,Ndim);
CCC_raw=zeros(1,Ndim);
ICC_raw=zeros(1,Ndim);
alpha_raw=zeros(1,Ndim);
for d=1:Ndim,
    [RMSE_raw(d),CC_raw(d),CCC_raw(d),ICC_raw(d),alpha_raw(d)] = raters_agreement([all_ratings{d,:}]);
end

%% perform CCC centring

fprintf('-> Perform CCC centring...\n');

all_ratings_CCC_cent=cell(Ndim,Nf);

%perform centring
for d=1:Ndim,
    for f=1:Nf,
        ratings=all_ratings{d,f};
        
        %compute agreement between pairs of raters with CCC
        CCC=zeros(1,Ncnk);
        for k=1:Ncnk,
            CCC(k) = CCC_calc(ratings(rater_cnk(k,1),:),ratings(rater_cnk(k,2),:));
        end
        
        %compute agreement for each rater
        CCC_agr=zeros(1,Nr);
        for r=1:Nr,
            CCC_agr(r)=mean(CCC(rater_appearance(:,r)));
        end
        
        %compute centring values
        mean_rating=mean(ratings,2)';
        wgh_ref_CCC=sum((mean_rating.*CCC_agr)/sum(CCC_agr));
        
        %perform centing
        all_ratings_CCC_cent{d,f}=all_ratings{d,f}-repmat(mean_rating',1,Nframe)+wgh_ref_CCC;
        
    end
end

%% compute agreement on centred ratings
fprintf('-> Compute inter-rater agreement on CCC centred...\n');
RMSE_CCC_cent=zeros(1,Ndim);
CC_CCC_cent=zeros(1,Ndim);
CCC_CCC_cent=zeros(1,Ndim);
ICC_CCC_cent=zeros(1,Ndim);
alpha_CCC_cent=zeros(1,Ndim);
for d=1:Ndim,
    [RMSE_CCC_cent(d),CC_CCC_cent(d),CCC_CCC_cent(d),ICC_CCC_cent(d),alpha_CCC_cent(d)] = raters_agreement([all_ratings_CCC_cent{d,:}]);
end

%% display statistics
fprintf('-> Results\n\n')

fprintf('\t\t|\tRMSE\t|\tCC\t\t|\tCCC\t\t|\tICC\t\t|\talpha\n');
fprintf('%s\n',repmat('_',1,70));
fprintf([repmat('\t',1,7),'Raw\n']);
fprintf('%s\n',repmat('_',1,70));
for d=1:Ndim,
    fprintf('%s\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\n',emo_dim{d},RMSE_raw(d),CC_raw(d),CCC_raw(d),ICC_raw(d),alpha_raw(d))
end
fprintf('%s\n',repmat('_',1,70));
fprintf([repmat('\t',1,6),'CCC centred\n']);
fprintf('%s\n',repmat('_',1,70));
for d=1:Ndim,
    fprintf('%s\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\t|\t%3.3f\n',emo_dim{d},RMSE_CCC_cent(d),CC_CCC_cent(d),CCC_CCC_cent(d),ICC_CCC_cent(d),alpha_CCC_cent(d))
end

%% read gold standard folder for visualisation of both
%
%uncomment this part to plot gold standard from original folder, and the
%one computed in this script - they are obsiously the same
%
% for d=1:Ndim,
%     for f=1:Nf,
%         [~,filename,~]=fileparts(files(f).name);
%         
%         %read provided gs
%         FID=fopen(fullfile(gs_path,emo_dim{d},[filename,'.arff']));
%         data=textscan(FID,'%s %f %f','Delimiter',{'\n',','},'HeaderLines',9);
%         fclose(FID);
%         gs=data{3}';
%         
%         %gs computed here
%         gold_standard_CCC_cent=mean(all_ratings_CCC_cent{d,f});
%         
%         %plot
%         plot(frametime,gs)
%         hold on,plot(frametime,gold_standard_CCC_cent,'r'),hold off
%         title(strrep(filename,'_',' '))
%         legend('Provided gold standard','Computed gold standard')
%         xlabel('time in seconds')
%         ylabel(emo_dim{d})
%         pause
%     end
% end
