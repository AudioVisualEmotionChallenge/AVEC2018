import GlobalsVars as v
import csv
import os
import arff
import numpy as np

#Return a collection countaining all CSV files in the form tab[Dimension][File]
def openingRatingIndividual():
	rGoldIndiv = {}
	files = listFiles()
	for i in range(v.nDim):
		 for f in files[i][0]:
			csvs = np.genfromtxt(files[i][1]+f, delimiter=';')
			if (rGoldIndiv.get(v.eName[i],None) == None):
				rGoldIndiv[v.eName[i]] = []
			rGoldIndiv[v.eName[i]].append(csvs)
	return rGoldIndiv
#End openingRatingIndividual

#Return the combinatory sequence of size k
#From : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=combinaisons
def combinListe(seq, k):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j<=jmax:
            if (i>>j)&1==1:
                s.append(seq[j])
            j += 1
        if len(s)==k:
            p.append(s)
        i += 1 
    return p
#End combinListe

#Calculate RMSE, CC and CCC for 2 tab
def ratersStatistics(r1,r2):
	#MSE
	mse = np.nanmean(np.power((r1-r2),2))
	#RMSE
	rmse = np.sqrt(mse)
	#CC
	r1Mean = np.nanmean(r1)
	r2Mean = np.nanmean(r2)
	r1Std = np.nanstd(r1)
	r2Std = np.nanstd(r2)
	covariance = np.nanmean(np.multiply((r1-r1Mean),(r2-r2Mean)));
	cc = covariance/(r1Std*r2Std);
	#CCC
	r1Var=pow(r1Std,2)
	r2Var=pow(r2Std,2)
	ccc=(2*covariance)/(r1Var+r2Var+pow((r1Mean-r2Mean),2))
	return rmse,cc,ccc
#End ratersStatistics

#List all the file in the goldStandard folder
def listFiles():
	files = []
	#We get a tab countaining each file
	for i, s in enumerate(v.agsi):
		files.append([sorted(os.listdir(s)),s])
	return files;
#End listFiles

#Return a tab that countain all stats measures sorted by dimension, audio file and then stats tab[dimension][audio][combinaison][stat] 
def ratersAgreement(rGoldIndiv, combnk, files):
	res = []
	#For each file and each combination of raters, we get statistics about there agreement on rating
	for i in range(v.nDim):
		statF = []
		for f, fname in enumerate(files[i][0]):
			stats = []
			for c in combnk:
				firstCsv = np.array(rGoldIndiv[v.eName[i]][f][1:,c[0]+1])
				secondCsv = np.array(rGoldIndiv[v.eName[i]][f][1:,c[1]+1])
				[rmse, cc, ccc] = ratersStatistics(firstCsv,secondCsv)
				stats.append([rmse, cc, ccc])
			statF.append(stats)
		res.append(statF)
	return res
#End ratersAgreement

#Return a tab containing for each rater his agreement (CCC) with the others tab[rater][dimension][file] = value
def raterAgreement(ra, combnk, files):
	aRa = []
	for a in range(v.nAn):
		rater = []
		for i in range(v.nDim):
			dimension = []
			for f, fname in enumerate(files[i][0]):
				valuesAgr = []
				for n in range(len(combnk)):
					ras = ra[i][f][n]
					#print ras[2]
					if (combnk[n][0] == a or combnk[n][1] == a):
						#We want only CCC
						valuesAgr.append(ras[2])
				#We add the mean in the tab
				#print f, fname, np.nanmean(valuesAgr)
				dimension.append(np.nanmean(valuesAgr))
			rater.append(dimension)
		aRa.append(rater)
	return np.array(aRa)
#End raterAgreement

#Center all the goldStandard
def cccCentring(ra, combnk, files, aRa, rGoldIndiv):
	for i in range(v.nDim):
		for f, fname in enumerate(files[i][0]):
			meanByF = []
			wghRater = []
			csv = rGoldIndiv[v.eName[i]][f]
			#Firstly we compute the mean of all raters for each file
			for a in range(v.nAn):
				#We get the mean
				meanRatersF = np.nanmean(csv[:,a+1])
				meanByF.append(meanRatersF)	
				#We take the weight of the rater in this file
				wghRater.append(aRa[a][i][f])
			#Now we calculate the ponderate mean of all raters
			pondMean = np.sum(np.multiply(meanByF,wghRater))/np.sum(aRa[:,i,f])
			#We have the mean of all raters, we need the total mean of the file
			meanF = np.nanmean(csv[:,1:])
			#Now we will center each prediction according to the mean
			output = []
			#We prepare the ARFF file, we get the template
			data = arff.load(open(v.arffTempPath,'rb'))
			for line in range(len(csv)-1):
				meanLine = np.nanmean(csv[line+1,1:])
				newGs = meanLine-meanF+pondMean
				#We replace the values in the ARFF template
				data["data"][line][0] = fname.replace(".csv","")
				data["data"][line][1] = round(csv[line+1,0],2)
				data["data"][line][2] = round(newGs,6)
			#We write the csv in the Gold Standard folder
			f = open(v.ags[i]+fname.replace(".csv",".arff"), "w")
			f.write(arff.dumps(data))	
	return None
#End cccCentring

def gsCreation():
	#We load ARFF files countaining ratings
	print("Reading individual ratings...")
	rGoldIndiv = openingRatingIndividual()
	print("Computing inter-rater agreement on raw...")
	seq = []
	for i in range(v.nAn):
		seq.append(i)
	#We take the combination list for each rater
	combnk = combinListe(seq,2)
	#We get the names of files
	files = listFiles()
	#We compute the agreement between each rater of this list
	ra = ratersAgreement(rGoldIndiv, combnk, files)
	#We compute the agreement of each rater
	aRa = raterAgreement(ra, combnk, files)
	#print aRa
	#print sum(aRa)
	print("Perform CCC centring...")
	cccCentring(ra, combnk, files, aRa, rGoldIndiv)
#End gsCreation

gsCreation()
