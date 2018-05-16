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

#Do the post treatement for test partition and save if there are better results
def postTreatTest(gs, pred, ccc, bias, scale, biasB, scaleB, nDim):
	gspt = {}
	for s in 'dev','test':
		gspt[s] = np.array(gs[s])[:,nDim]
		if (biasB == True):
			#We add the bias to the prediction and save if there is an improvement
			pred[s] = np.array(pred[s]) + bias
			ccc[s] = cccCalc(pred[s],gs[s])
		if (scaleB == True):
			#We apply the scale and save if improvement
			pred[s] = np.multiply(pred[s],scale)
			ccc[s] = cccCalc(pred[s],gs[s])
	return ccc, pred
#End postTreatementTest	

#Do the post treatement for dev partition and save if there are better results
def postTreatDev(cccDev, pred, gs, earlystop):
	gsDev = np.array(gs['dev'])
	#[0] = Arousal/[1] = Valence
	[bias, cccSave, scale] = [[] for i in range(3)]
	biasB, scaleB = False, False
	for nDim in range(v.nDim):
		if (earlystop[nDim] != 0):
			#We save the ccc from Dev
			cccSave.append(cccDev[nDim])
			#First we calculate the bias
			gsDevMean = np.nanmean(gsDev[:,nDim])
			predMean = np.nanmean(pred[nDim])
			bias.append(gsDevMean - predMean)
			#We add the bias to the prediction and save if there is an improvement
			predCenter = pred[nDim] + bias[nDim]
			cccBias = cccCalc(predCenter,gsDev[:,nDim])
			if (cccBias > cccSave[nDim]):
				cccSave[nDim] = cccBias
				pred[nDim] = predCenter
				biasB = True
			#We now scale the prediction and do the same thing
			#First we calculate the scale
			stdGs = np.nanstd(gsDev[:,nDim])
			stdPred = np.nanstd(pred[nDim])
			scale.append(stdGs/stdPred)
			#We apply the scale and save if improvement
			predScale = np.multiply(pred[nDim],scale[nDim])
			cccScale = cccCalc(predScale,gsDev[:,nDim])
			if (cccScale > cccSave[nDim]) :
				cccSave[nDim] = cccScale
				pred[nDim] = predScale
				scaleB = True
		else :
			cccSave.append(-1.0)
			bias.append(-1.0)
			scale.append(-1.0)
	return cccSave, biasB, scaleB, bias, scale
#End postTratementDev
