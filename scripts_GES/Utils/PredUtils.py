import GlobalsVars as v
import arff
import os
import numpy as np
import sys
import scipy as sp
from scipy import signal
import timeit

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

#Remove the first and last column of a ARFF matrix
def removeColArff(arff):
	arff['attributes'] = arff['attributes'][1:-1]
	arff['data'] = np.array(arff['data'])[:,1:-1]
	return arff	
#Fin removeColArff

#Put to 0 NaN values in ARFF
def nanToZero(arff):
	for ind, att in enumerate(arff['attributes']):
		for val in arff['data']:
			if (np.isnan(val[ind])):
				val[ind] = 0
	return arff

def unimodalPredPrep(wSize, wStep):
	#We open corresponding files
	train = arff.load(open(v.audioDesc+"Norm/"+v.fconf+"_train_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	dev = arff.load(open(v.audioDesc+"Norm/"+v.fconf+"_dev_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	test = arff.load(open(v.audioDesc+"Norm/"+v.fconf+"_test_"+str(wSize)+"_"+str(wStep)+"_norm.arff","rb"))
	#We remove first and last column
	train = removeColArff(train)
	dev = removeColArff(dev)
	test = removeColArff(test)
	#We put to 0 NaN values
	train = nanToZero(train)
	dev = nanToZero(dev)
	test = nanToZero(test)
	#We transform it in array
	tr = np.array(train['data'])
	de = np.array(dev['data'])
	te = np.array(test['data'])
	return tr,de,te
