#Author: Adrien Michaud
import GlobalsVars as v
from PredUtils import cccCalc
import arff
import os
import numpy as np
import sys
import scipy as sp
sys.path.append(v.labLinearPath)
import liblinearutil as llu

#Do the post treatement for test partition and save it
def postTreatTest(gs, pred, ccc, bias, scale, nDim):
	for s in 'dev','test':
		gspt = np.array(gs[s])[:,nDim]
		if (bias != 0.0):
			#We add the bias to the prediction and save if there is an improvement
			pred[s] = np.array(pred[s]) + bias
			ccc[s] = cccCalc(pred[s],gspt)
		if (scale != 0.0):
			#We apply the scale and save if improvement
			pred[s] = np.multiply(pred[s],scale)
			ccc[s] = cccCalc(pred[s],gspt)
	return ccc, pred
#End postTreatementTest	

#Do the post treatement for dev partition and save if there are better results
def postTreatDev(ccc, pred, gs, nDim):
	gsDev = np.array(gs['dev'])[:,nDim]
	#First we calculate the bias
	gsDevMean = np.nanmean(gsDev)
	predMean = np.nanmean(pred)
	bias = gsDevMean - predMean
	#We add the bias to the prediction and save if there is an improvement
	predCenter = pred + bias
	cccBias = cccCalc(predCenter,gsDev)
	if (cccBias > ccc):
		ccc = cccBias
		pred = predCenter
	else :
		bias = 0.0
	#We now scale the prediction and do the same thing
	#First we calculate the scale
	stdGs = np.nanstd(gsDev)
	stdPred = np.nanstd(pred)
	scale = stdGs/stdPred
	#We apply the scale and save if improvement
	predScale = np.multiply(pred,scale)
	cccScale = cccCalc(predScale,gsDev)
	if (cccScale > ccc) :
		ccc = cccScale
		pred = predScale
	else :
		scale = 0.0
	return ccc, pred, bias, scale
#End postTreatementDev
