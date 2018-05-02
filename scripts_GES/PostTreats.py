import GlobalsVars as v
from GSMatching import cccCalc
import arff
import os
import numpy as np
import sys
import scipy as sp
sys.path.append(v.labLinearPath)
import liblinearutil as llu

#Do the post treatement for test partition and save if there are better results
def postTreatTest(pred, gs, ccc, bias, scale, biasB, scaleB, nDim):
	gsT = np.array(gs['test'])[:,nDim]
	#We save the ccc from Test
	cccSave = ccc
	if (biasB == True):
		#We add the bias to the prediction and save if there is an improvement
		predCenter = np.array(pred) + bias
		cccBias = cccCalc(predCenter,gsT)
		if (cccBias > cccSave):
			cccSave = cccBias
			biasB = True
	if (scaleB == True):
		#We apply the scale and save if improvement
		predScale = np.multiply(pred,scale)
		cccScale = cccCalc(predCenter,gsT)
		if (cccScale > cccSave) :
			cccSave = cccScale
			scaleB = True
	return cccSave
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
				scaleB = True
		else :
			cccSave.append(-1.0)
			bias.append(-1.0)
			scale.append(-1.0)
	return cccSave, biasB, scaleB, bias, scale
#End postTratementDev
