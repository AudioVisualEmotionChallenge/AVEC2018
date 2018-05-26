#Author: Adrien Michaud
import sys
import numpy as np
import scipy as sp
import timeit
import copy
import cPickle
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from sklearn import linear_model
from Setup import setup
from LinearRegression import regression
from NormConc import normFeatures, concGs, concFeats
from PredUtils import unimodalPredPrep, cccCalc, cutTabs, predMulti, saveObject, restaurObject, initTabData, unimodalPred
from Print import printValTest
from GSMatching import gsOpen, gsMatch

#Do the post treatement for test partition and save it
def postTreatTest(gs, pred, ccc, bias, scale, nDim):
	for s in v.aPart :
		gspt = np.array(gs[s])[nDim]
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

#Predict on test the best values found with Dev and print the results
def predictTest():
	bestVals = restaurObject("../Pred/BestValues.obj")
	#Concatenation of Gold Standards
	concGs(True)
	#Tab for the linear regression
	datas = initTabData()
	print(v.goodColor+"Test prediction in progress..."+v.endColor)
	for nMod in range(len(v.desc)):
		for nDim in range(len(v.eName)):
			bVals = bestVals[v.nameMod[nMod]][nDim]
			#Value/wSize/wStep/Delay/Complexity/BiasUse/ScaleUse/BiasValue/ScaleValue
			wSize = float(bVals[1])
			wStep = float(bVals[2])
			dl = float(bVals[4])
			c = float(bVals[5])
			bias = float(bVals[6])
			scale = float(bVals[7])
			#Concatenation of ARFF data
			concFeats(wSize, wStep, nMod)
			#Normalisation of Features
			normFeatures(wSize, wStep, nMod)
			#We open the files for the unimodal prediction
			feats = unimodalPredPrep(wSize, wStep, nMod)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(v.matchGS[1], dl, wSize, nMod, True)
			#We do the prediction on Dev/Test
			[cccs, preds, function, alpha] = unimodalPred(gs, feats, nDim, True)
			#Post-treatement
			[cccs, preds] = postTreatTest(gs, preds, cccs, bias, scale, nDim)
			#We save the predictions/cccs and GS
			for s in v.aPart :
				datas[s][nDim][nMod] = preds[s]
				if (len(datas['gs'+s][nDim]) == 0 or len(datas['gs'+s][nDim]) > len(gs[s][nDim])):
					datas['gs'+s][nDim] = gs[s][nDim]
			datas['cccs'][nDim][nMod] = [[round(cccs['dev'],3), round(cccs['test'],3)], round(wSize,2), round(wStep,2), round(dl,2), alpha, bias, scale, function]
			printValTest(datas['cccs'],nMod, nDim)
	saveObject(datas,"./datas.obj")
	datas = restaurObject("./datas.obj")
	regression(datas, True)
#End predictTest

def main():
	endOrNot = setup(True)
	if (endOrNot == True):
		for i in range(len(sys.argv)):
			if (sys.argv[i] == "--debug" or sys.argv[i] == "debug"):
				v.debugMode = True
		predictTest()
	else :
		print ("Error on setup, please check files")

main()
