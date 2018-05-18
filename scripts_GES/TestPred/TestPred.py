#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from LinearRegression import linearRegression
from ConcArff import concGs, concRec
from FeatsNorm import normFeatures
from PostTreats import postTreatTest
from PredUtils import unimodalPredPrep, cccCalc, cutTab, predMulti
from Print import printValTest, bestLinearRegression
from GSMatching import gsOpen, gsMatch
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict
from sklearn import linear_model
import numpy as np
import scipy as sp
import timeit
import cPickle

#Unimodal prediction on Test partition
def unimodalPredTest(gs, c, feat, nDim):
	gsu = {}
	pred = {}
	ccc = {}
	for s in v.part:
		gsu[s] = np.array(gs[s])[:,nDim]
	#Options for liblinear
	options = "-s "+str(v.sVal)+" -c "+str(c)+" -B 1 -q"
	#We learn the model on train
	model = train(gsu['train'],feat['train'],options)
	#We predict on test data
	for s in v.part:
		pred[s] = np.array(predict(gsu[s],feat[s],model,"-q"))[0]
		#We calculate the correlation and store it
		ccc[s] = cccCalc(np.array(pred[s]),gsu[s])
	return ccc, pred, gsu
#Fin unimodalPredictionDev

#Predict on test the best values found with Dev and print the results
def predictTest():
	bestVals=cPickle.load(open("../Pred/BestValues.txt"))
	#Concatenation of Gold Standards
	concGs(True)
	#Tab for the linear regression
	preds = {}
	gsPart = {}
	for s in v.aPart :
		preds[s] = []
		for nDim in range(len(v.eName)):
			preds[s].append([])
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
			#Var for storing differents CCC
			ccc = []
			#Concatenation of ARFF data
			concRec(wSize, wStep, nMod)
			#Normalisation of Features
			normFeatures(wSize, wStep, nMod)
			#We open the files for the unimodal prediction
			[feats,trainLen] = unimodalPredPrep(wSize, wStep, nMod)
			#We open the files for the Gold Standard Matching
			gsBase = gsOpen(wSize, True)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(v.matchGS[0], dl, wSize, gsBase, trainLen,True)
			#We do the prediction on Dev/Test
			[ccc, pred, gsu] = unimodalPredTest(gs, c, feats, nDim)
			#Post-treatement
			[ccc, pred] = postTreatTest(gs, pred, ccc, bias, scale, nDim)
			#We save the predictions and GS
			for s in v.aPart :
				preds[s][nDim].append(pred[s])
				if (gsPart.get(s,None) == None or len(gsPart[s]) > len(gs[s])):
					gsPart[s] = gs[s]
			#We store the results
			ccc = [nDim, round(ccc['dev'],3), round(ccc['test'],3), round(wSize,2), round(wStep,2), round(dl,2), c, v.matchGS[0], bias, scale]
			printValTest(ccc,nMod)
	results = linearRegression(preds, gsPart)
	bestLinearRegression(results)
#End predictTest
