function [a,R,N]=cronbach(X)
% CRONBACH Cronbach's Alpha
%   [a,R,N]=cronbach(X) calculates the Cronbach's alpha of the data set X.
%
%   a is the Cronbach's alpha.
%   R is the upper triangular Spearman inter-correlation matrix
%   N is the number of vald items
%   X is the data set. Columns are the items.
%
%
%   Reference:
%   Cronbach L J (1951): Coefficient alpha and the internal structure of
%   tests. Psychometrika 16:297-333
%
%
%   If there are items with zero variance, these itemns are excluded from
%   the calculation. There is a warning in this case; alpha might be
%   guessed to high.
%
%
% Frederik Nagel
% Institute of Music Physiology and Musicians' Medicine
% Hanover University of Music and Drama 
% Hannover
% Germany
%
% e-mail: frederik.nagel@hmt-hannover.de
% homepage: http://www.immm.hmt-hannover.de
%
% April 24, 2006.



if nargin<1 || isempty(X)
   error('You shoud provide a data set.');
else
   % X must be at least a 2 dimensional matrix
   if size(X,2)<2
      error('Invalid data set.');
   end
   if size(X,1)<size(X,2),X=X';end
end
% Items
N=size(X,2);

% Entries of the upper triangular matrix
e=(N*(N-1)/2);

% Spearman's correlation coefficient
R = corr(X,'rows','pairwise','type','spearman');

% Coefficients from upper triangular matrix
R = triu(R,1);   

% Mean of correlation coefficients
r = sum(sum(triu(R,1)))/e;

% If there are columns with zero variance, these have to be excluded.
if(isnan(r))
    disp('There are columns with zero variance!');
    disp('These columns have been excluded from the calculation of alpha!');        
    disp([num2str(sum(sum(isnan(R)))) ' coefficients of ' num2str(N*N) ' have been excluded.']);    

    % Correct # of items 
    e = e-sum(sum(isnan(R)));
    
    % corrected mean of correlation coefficients 
    r = nansum(nansum(R))/e;    
    
    % corrected number of items
    N = N - sum(isnan(R(1,:)));
end
% Formular for alpha (Cronbach 1951)
a=(N*r)/(1+(N-1)*r);