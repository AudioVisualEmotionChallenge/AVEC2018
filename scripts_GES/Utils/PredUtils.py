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
import timeit
import cPickle
from scipy import signal
from sklearn import linear_model

#Used to create the tab countaining all datas
def initTabData():
	datas = {}
	for s in 'dev','test','cccs','gstrain','gsdev','gstest':
		datas[s] = []
	for nDim in range(len(v.eName)):
		for s in 'dev','test','cccs','gstrain','gsdev','gstest':
			datas[s].append([])
		for nMod in range(len(v.desc)):
			for s in 'dev','test','cccs' :
				datas[s][nDim].append([])
	return datas
#End initTabData

#Save an object on the disk using cPickle module
def saveObject(obj, addr):
	f = open(addr,"wb")
	cPickle.dump(obj, f)
	f.close()
#End saveObject

#Restaure an object saved on the disk using cPickle module
def restaurObject(addr):
	f = open(addr,"rb")
	obj = cPickle.load(f)
	f.close()
	return obj
#End restaurObject

#Augment the tab to take context
def tabContext(datas, cMode, cSize):
	tab = []
	for i in range(len(datas)):
		temp = []
		for j in range(cSize):
			if (cMode == "left"):
				ind = i-j
			elif (cMode == "right"):
				ind = i+cSize-j
			else :
				ind = i+int(cSize/2)-j
			if (ind < 0):
				ind = 0
			elif (ind > len(datas)-1):
				ind = len(datas)-1
			temp.append(datas[ind])
		tab.append(temp)
	return tab
#End tabContext			

#Cut a tab to a size given
def cutTab(tab,size):
	lTab = len(tab)
	oneF = int(size/9)
	if (lTab != size):
		temp = []
		for i in range(v.nbFPart):
			for j in range(oneF):
				ind = (int(lTab/9)*i)+j-1
				temp.append(tab[ind])
		tab = temp
	return tab
#End cutTab

#Used to uniformize tab
def cutTabs(datas, part):
	#First we uniformize the GS
	minSize = 0
	for nDim in range(len(v.eName)):
		for s in part :
			if (minSize > len(datas['gs'+s][nDim]) or minSize == 0):
				minSize = len(datas['gs'+s][nDim])
	oneF = int(minSize/9)
	#We cut all tab to reach this size
	for nDim in range(len(v.eName)):
		for s in part :
			#Gold Standard Tab
			datas['gs'+s][nDim] = cutTab(datas['gs'+s][nDim],minSize)
			#Predictions tab
			for nMod in range(len(v.desc)):
				datas[s][nDim][nMod] = cutTab(datas[s][nDim][nMod],minSize)
	return datas
#End cutTabs

#Used to resample the tab
def resamplingTab(tab, size):
	if (len(tab) != size):
		s = signal.resample(tab,size)
		return s
	else :
		return tab
#End resamplingTab

#Calculus of CCC
def cccCalc(pred,ref):
	if (len(pred) == len(ref)):
		if (v.cccMode == 0):
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
		else :
			oneF = len(pred)/v.nbFPart
			cccs = []
			for i in range(v.nbFPart):
				predTemp = pred[(i*oneF):(i*oneF+oneF-1)]
				refTemp = ref[(i*oneF):(i*oneF+oneF-1)]
				predMean = np.nanmean(predTemp)
				refMean = np.nanmean(refTemp)
				predVar = np.nanvar(predTemp)
				refVar = np.nanvar(refTemp)
				predV = (predTemp-predMean)
				refV = (refTemp-refMean)
				predRef = np.multiply(predV,refV)
				covariance = np.nanmean(predRef)
				ccc = (2*covariance)/(predVar+refVar+pow((predMean-refMean),2))
				cccs.append(ccc)
			return np.nanmean(cccs)
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
def predMulti(coef, preds, nDim, funcType, cSize):
	pred = []
	for i in range(len(preds[nDim][0])):
		p = 0
		if (funcType == 0):
			for nMod in range(len(preds[nDim])):
				for size in range(cSize):
					ind = size*nMod+nMod
					p += coef[ind]*preds[nDim][nMod][i][size]
		else:
			for dim in range(len(v.eName)):
				for nMod in range(len(preds[nDim])):
					for size in range(cSize):
						nbMod = len(preds[nDim])
						ind = (nMod*cSize)+size
						p+= coef[dim][ind]*preds[dim][nMod][i][size]
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

#Load and prepare files for the unimodal prediction
def unimodalPredPrep(wSize, wStep, nMod):
	feats = {}
	#We need the number of line for a wStep of v.tsp
	trainLen = len(arff.load(open(v.descNorm[nMod]+"train_"+str(wSize)+"_"+str(v.tsp)+".arff","rb"))['data'])
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
#End unimodalPredPrep

def isInt(string, limit):
	for i in range(limit):
		if (string == str(i)):
			return True
	return False
