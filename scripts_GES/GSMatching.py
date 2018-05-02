import GlobalsVars as v
import arff
import os
import numpy as np
import sys
sys.path.append(v.labLinearPath)
import liblinearutil as llu

#Open the differents ARFF needed for the matching
def gsOpen(wSize,wStep):
	ar = {}
	va = {}
	d = {}
	for s in "dev","train","test":
		ar[s] = arff.load(open(v.TODODODODOD+s+"_arousal.arff","rb"))
		va[s] = arff.load(open(v.TODODODODOD+s+"_valence.arff","rb"))
		d[s] = arff.load(open(v.TODODODODOD+v.fconf+"_"+s+"_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	return ar,va,d
#End goldStandardOpen

#Apply the gold standards to the differents parameters and treatments
def gsMatch(method, dl, wSize, wStep, art, vat, dt):
	#Tab who will countain the matching
	vGoldS = {}
	for s in "dev","train","test":
		ar = art[s]
		va = vat[s]
		d = dt[s]
		#In the concatenate file, we have 9 files
		tFD = len(d['data'])/9
		tFS = len(ar['data'])/9
		#We get the data for each 9 files
		for i in range(9):
			#For all the value of a file
			for j in range(tFD):
				#The central method is : we take the mid point of earch window
				if (method == "central"):
					calcul = (((float(wSize)/2.0)+wStep*float(j)+dl)/v.ts)+float(tFS*i)
					ind = int(calcul)
					if (ind >= tFS+tFS*i):
						ind = tFS+tFS*i-1
					vals = [ar['data'][ind][2],va['data'][ind][2]]
				#Else we use the mean method : we do the mean of each value in the window 
				else :	
					calcul = ((wStep*float(j)+dl)/v.ts)+float(tFS*i)
					ind = int(calcul)
					indA = ind+int((float(wSize)/v.ts))
					if (ind >= tFS+tFS*i):
						ind = tFS+tFS*i-1
					if (indA >= tFS+tFS*i):
						indA = tFS+tFS*i-1
					if (indA != ind):
						moy = [0.0,0.0]
						for k in range(ind, indA):
							moy[0] += ar['data'][k][2]
							moy[1] += va['data'][k][2]
						vals = [moy[0]/(indA-ind),moy[1]/(indA-ind)]
					else:
						vals = [ar['data'][ind][2],va['data'][ind][2]]
				if (vGoldS.get(s+"_ind",None) == None):
					vGoldS[s] = []
				vGoldS[s+"_ind"] = ind
				if (vGoldS.get(s,None) == None):
					vGoldS[s] = []
				vGoldS[s].append(vals)
	return vGoldS
#End goldStandardMatch : return a tab countaining the matching

#Calculus of CCC
def cccCalc(pred,ref):
	if (len(pred) == len(ref)):
		predMean = np.nanmean(pred)
		refMean = np.nanmean(ref)
		predVar = np.nanvar(pred)
		refVar = np.nanvar(ref)
		predV = (pred-predMean)
		refV = (ref-refMean)
		predRef = np.multiply(predV,refV)
		covariance = np.nanmean(predRef)
		ccc = (2*covariance)/(predVar+refVar+pow((predMean-refMean),2))
		return ccc
	else:
		print "Size of pred and ref are not the same"
		return 0.0
#End cccCalc
