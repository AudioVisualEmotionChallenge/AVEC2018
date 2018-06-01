#Author: Adrien Michaud
import sys
import numpy as np
import scipy as sp
import timeit
import copy
import warnings
import cPickle
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from sklearn import linear_model
from Setup import setup
from LinearRegression import regression
from sklearn.exceptions import ConvergenceWarning
from NormConc import normFeatures, concGs, concFeats
from PredUtils import unimodalPredPrep, cccCalc, cutTabs, predMulti, saveObject, restaurObject, initTabData
from Print import printValTest
from GSMatching import gsOpen, gsMatch
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict


def unimodalPredTest(gs, feats, nDim, func, c):
	warnings.filterwarnings('ignore', category=ConvergenceWarning)
	if (func == "SVR"):
		#Options for liblinear
		options = "-s "+str(v.sVal)+" -c "+str(c)+" -B 1 -q"
		#We learn the model on train
		model = train(gs['train'][nDim],feats['train'],options)
		#We predict on data
		for s in v.aPart:
			pred = np.array(predict(gs[s][nDim],feats[s],model,"-q"))[0]
			#We calculate the correlation and store it
			ccc = cccCalc(np.array(pred),gs[s][nDim])
			if (ccc > cccs[s]):
				preds[s] = pred
				cccs[s] = ccc
	else :
		fun = None
		funT = None
		for f in range(len(v.lFunc)):
			if (f[2] == func):
				fun = f[0]
				funT = f[1]
		reg = func[0](alpha=c)
		if (func[1] == 0):
			reg.fit(feats['train'],gs['train'][nDim])
			for s in v.aPart:
				p = reg.predict(feats['dev'])
				ccc = cccCalc(p,gs[s][nDim])
				if (ccc > cccs[s]) : 
					preds[s] = p
					cccs[s] = ccc
		else:
			reg.fit(feats['train'],np.transpose(gs['train']))
			for s in parts:
				p = reg.predict(feats['dev'])[:,nDim]
				ccc = cccCalc(p,gs[s][nDim])
				if (ccc > cccs[s]) : 
					preds[s] = p
					cccs[s] = ccc
	return cccs, preds, func, c

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
			func = str(bVals[8])
			#Concatenation of ARFF data
			concFeats(wSize, wStep, nMod)
			#Normalisation of Features
			normFeatures(wSize, wStep, nMod)
			#We open the files for the unimodal prediction
			[feats, trainLen] = unimodalPredPrep(wSize, wStep, nMod)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(v.matchGS[1], dl, wSize, nMod, trainLen,True)
			#We do the prediction on Dev/Test
			[cccs, preds, function, alpha] = unimodalPredTest(gs, feats, nDim, func, c)
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
