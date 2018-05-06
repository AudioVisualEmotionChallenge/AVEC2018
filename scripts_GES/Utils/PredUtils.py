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
	return signal.resample(tab,size)
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
def removeColArff(arff, nMod):
	ind = 0;
	while (ind < len(arff['attributes'])):
		remove = False
		for i in range(len(v.removedColArff[nMod])):
			if (arff['attributes'][ind][0] == v.removedColArff[nMod][i]):
				arff['attributes'] = np.delete(arff['attributes'],ind,0)
				arff['data'] = np.delete(arff['data'],ind,1)
				remove = True
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
	train = arff.load(open(v.descNorm[nMod]+v.fconf[nMod]+"_train_"+str(wSize)+"_"+str(v.tsp)+"_norm.arff","rb"))
	trainLen = len(train['data'])
	#We open corresponding files
	train = arff.load(open(v.descNorm[nMod]+v.fconf[nMod]+"_train_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	dev = arff.load(open(v.descNorm[nMod]+v.fconf[nMod]+"_dev_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	test = arff.load(open(v.descNorm[nMod]+v.fconf[nMod]+"_test_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	#We remove column that are not good
	train = removeColArff(train, nMod)
	dev = removeColArff(dev, nMod)
	test = removeColArff(test, nMod)
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
