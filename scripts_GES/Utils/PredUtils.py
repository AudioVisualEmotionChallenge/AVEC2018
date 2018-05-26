#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
import arff
import os
import subprocess
import warnings
import time
import numpy as np
import sys
import scipy as sp
import timeit
import cPickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy import signal
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict
from sklearn import linear_model
from sklearn.exceptions import ConvergenceWarning

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
def predMulti(coef, preds, nDim, funcType):
	pred = []
	for i in range(len(preds[nDim][0])):
		p = 0
		if (funcType == 0):
			for nMod in range(len(preds[nDim])):
				p += coef[nMod]*preds[nDim][nMod][i]
		else:
			for dim in range(len(v.eName)):
				for nMod in range(len(preds[nDim])):
					p+= coef[nDim][nMod+dim*len(preds[nDim])]*preds[dim][nMod][i]
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
	return feats
#End unimodalPredPrep

#Unimodal prediction on partitions
def unimodalPred(gs, feats, nDim, modeTest):
	if (modeTest == True):
		parts = ['dev','test']
	else :
		parts = ['dev']
	[cccs, preds] = [{} for i in range(2)]
	for s in parts:
		cccs[s] = -1.0
	#Liblinear
	for comp in v.C:
		#Options for liblinear
		options = "-s "+str(v.sVal)+" -c "+str(comp)+" -B 1 -q"
		#We learn the model on train
		model = train(gs['train'][nDim],feats['train'],options)
		#We predict on data
		for s in parts:
			pred = np.array(predict(gs[s][nDim],feats[s],model,"-q"))[0]
			#We calculate the correlation and store it
			ccc = cccCalc(np.array(pred),gs[s][nDim])
			if (ccc > cccs[s]):
				preds[s] = pred
				cccs[s] = ccc
				function = "SVR"
				alpha = comp
	#We see if we can do better with sklearn
	for nbFunc in range(len(v.lFunc)):
		#tab = []
		#tab2 = []
		for c in v.parFunc[nbFunc]:
			func = v.lFunc[nbFunc]
			reg = func[0](alpha=c)
			warnings.filterwarnings('ignore', category=ConvergenceWarning)
			#One task prediction
			if (func[1] == 0):
				reg.fit(feats['train'],gs['train'][nDim])
				for s in parts:
					p = reg.predict(feats['dev'])
					ccc = cccCalc(p,gs[s][nDim])
					if (ccc > cccs[s]) : 
						preds[s] = p
						cccs[s] = ccc
						function = func[2]
						alpha = c
			#Multi task prediction
			else :
				reg.fit(feats['train'],np.transpose(gs['train']))
				for s in parts:
					p = reg.predict(feats['dev'])[:,nDim]
					ccc = cccCalc(p,gs[s][nDim])
					if (ccc > cccs[s]) : 
						preds[s] = p
						cccs[s] = ccc
						function = func[2]
						alpha = c
			#tab.append(round(ccc,3))
			#tab2.append(c)
		#N = len(np.array(tab2))
		#x2 = np.arange(N)
		#colorspec = [[1,1,0],[1,0,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]]
		#if (v.x < 5):
		#	plt.plot(x2,np.array(tab), label=str(func[2]), color=colorspec[nbFunc],linewidth=0.1, marker='o',linestyle='dashed')
		#	v.x += 1
		#else :
		#	plt.plot(x2,np.array(tab), color=colorspec[nbFunc], marker='o',linewidth=0.3,markersize=0.5,linestyle='dashed')
		#plt.legend(loc='lower right')
		#plt.title("CCC with alpha decrease by linear model")
		#plt.xticks(x2,np.array(tab2))
		#f = open("../Figures/plotSCR.png","wb")
		#plt.savefig(f)
		#f.close()
		#print "plt saved"
	return cccs, preds, function, alpha
#Fin unimodalPred

def isInt(string, limit):
	for i in range(limit):
		if (string == str(i)):
			return True
	return False