#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
import arff
import os
import subprocess
import time
import numpy as np
import sys
import scipy as sp
from scipy import signal
import timeit

#Used to resample the tab
def resamplingTab(tab, size):
	#t = []
	#for i in range(size):
	#	ind = int(float(len(tab)/size)*float(i))
	# 	t.append(tab[ind])
	s = signal.resample(tab,size)
	#for i in range(len(s)):
	#	print tab
	#	if (s[i] > 1 or s[i] < -1):
	#		print s[i]
	return s
	#return t 
#End resamplingTab

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

#Remove the column that are not necessary in ARFF
def removeColArff(arff):
	ind = 0;
	lenght = len(arff['attributes'])
	while (ind < len(arff['attributes'])):
		remove = False
		for i in range(len(v.removedColArff)):
			if (ind == len(arff['attributes'])):
				break
			if (arff['attributes'][ind][0] == v.removedColArff[i]):
				del(arff['attributes'][ind])
				arff['data'] = np.delete(arff['data'],ind,1)
				remove = True
				lenght = len(arff['attributes'])
		if (remove == False) :
			ind += 1
	return arff	
#Fin removeColArff

#Put to 0 NaN values in ARFF
def arffNan(arff):
	for ind, att in enumerate(arff['attributes']):
		for val in arff['data']:
			if (val[ind] == "?" or val[ind] == None or val[ind] == np.nan):
				val[ind] = 0.0
	return arff

#Put to NaN ? or None values in ARFF:
def arffToNan(arff):
	for ind, att in enumerate(arff['attributes']):
		for val in arff['data']:
			if (val[ind] == "?" or val[ind] == None):
				val[ind] = np.nan
	return arff

def unimodalPredPrep(wSize, wStep, nMod):
	#We need the number of line for a wStep of v.tsp
	train = arff.load(open(v.descNorm[nMod]+"train_"+str(wSize)+"_"+str(v.tsp)+".arff","rb"))
	trainLen = len(train['data'])
	#We open corresponding files
	train = arff.load(open(v.descNorm[nMod]+"train_"+str(wSize)+"_"+str(wStep)+".arff","rb"))
	dev = arff.load(open(v.descNorm[nMod]+"dev_"+str(wSize)+"_"+str(wStep)+".arff","rb"))
	test = arff.load(open(v.descNorm[nMod]+"test_"+str(wSize)+"_"+str(wStep)+".arff","rb"))
	#We put to 0 NaN values
	train = arffNan(train)
	dev = arffNan(dev)
	test = arffNan(test)
	#We transform it in array
	tr = np.array(train['data'])
	de = np.array(dev['data'])
	te = np.array(test['data'])
	#We resample it to be at a wSize of v.tsp
	tr = resamplingTab(tr, trainLen)
	de = resamplingTab(de, trainLen)
	te = resamplingTab(te, trainLen)
	return tr,de,te
