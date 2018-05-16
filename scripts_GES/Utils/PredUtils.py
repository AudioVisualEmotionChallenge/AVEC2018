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

#Used to uniformize tab
def cutTab(tab):
	for nDim in range(len(v.eName)):
		#First we get the min size of the dimension
		minTab = 0
		for nMod in range(len(v.desc)):
			if (len(tab[nDim][nMod]) < minTab or minTab == 0):
				minTab = len(tab[nDim][nMod])
		#We need now to cut all tab to reach this size
		for nMod in range(len(v.desc)):
			oneF = int(minTab/9)
			lTabC = len(tab[nDim][nMod])
			temp = []
			for i in range(v.nbFPart):
				#We copy the elements
				for j in range(oneF):
					ind = (int(lTabC/9)*i)+j
					temp.append(tab[nDim][nMod][ind])
			tab[nDim][nMod] = temp
	return tab
#End cutTab
		

#Used to resample the tab
def resamplingTab(tab, size):
	#t = []
	#for i in range(size):
	#	ind = int(float(len(tab)/size)*float(i))
	# 	t.append(tab[ind])
	#return t 
	if (len(tab) != size):
		s = signal.resample(tab,size)
		return s
	else :
		return tab
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
			if (str(arff['attributes'][ind][0]) == str(v.removedColArff[i])):
				del(arff['attributes'][ind])
				arff['data'] = np.delete(arff['data'],ind,1)
				remove = True
				lenght = len(arff['attributes'])
		if (remove == False) :
			ind += 1
	return arff	
#Fin removeColArff

#Returning the multimodal prediction according to coef
def predMulti(coef, preds):
	pred = []
	for i in range(len(preds[0])):
		p = 0
		for nMod in range(len(v.desc)):
			p += coef[nMod]*preds[nMod][i]
		pred.append(p)
	return pred
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
	feats = {}
	#We need the number of line for a wStep of v.tsp
	train = arff.load(open(v.descNorm[nMod]+"train_"+str(wSize)+"_"+str(v.tsp)+".arff","rb"))
	trainLen = len(train['data'])
	print trainLen
	#We open corresponding files
	for s in v.part:	
		feats[s] = arff.load(open(v.descNorm[nMod]+s+"_"+str(wSize)+"_"+str(wStep)+".arff","rb"))
		#We put to 0 NaN values
		feats[s] = arffNan(feats[s])
		#We transform it in array
		feats[s] = np.array(feats[s]['data'])
		#We resample it to be at a wSize of v.tsp
		feats[s] = resamplingTab(feats[s], trainLen)
	return feats, trainLen
