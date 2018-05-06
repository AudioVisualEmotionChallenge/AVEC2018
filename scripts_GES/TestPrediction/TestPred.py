import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from ConcArff import concGs, concRec
from FeatsNorm import normFeatures
from PostTreats import postTreatTest
from PredUtils import unimodalPredPrep, cccCalc
from Print import printValTest
from GSMatching import gsOpen, gsMatch
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict
import numpy as np
import scipy as sp
import timeit

#Unimodal prediction on Test partition
def unimodalPredTest(gs, c, tr, te, de, nDim):
	gsTe = np.array(gs['test'])[:,nDim]
	gsDe = np.array(gs['dev'])[:,nDim]
	gsTr = np.array(gs['train'])[:,nDim]
	#Options for liblinear
	options = "-s "+str(v.sVal)+" -c "+str(c)+" -B 1 -q"
	#We learn the model on train
	model = train(gsTr,tr,options)
	#We predict on test data
	predTest = np.array(predict(gsTe,te,model,"-q"))[0]
	predDev = np.array(predict(gsDe,de,model,"-q"))[0]
	#We calculate the correlation and store it
	cccTest = cccCalc(np.array(predTest),gsTe)
	cccDev = cccCalc(np.array(predDev),gsDe)
	return cccTest, predTest, cccDev, predDev
#Fin unimodalPredictionDev

#Predict on test the best values found with Dev and print the results
def predictTest(nMod):
	#Concatenation of Gold Standards
	concGs(True)
	for nMod in range(len(v.desc)):
		for nDim in range(len(v.bAudio)):
			bVals = v.bVals[nMod][nDim]
			#Value/wSize/wStep/Delay/Complexity/MethodMatching/BiasUse/ScaleUse/BiasValue/ScaleValue
			wSize = bVals[1]
			wStep = bVals[2]
			dl = bVals[3]
			c = bVals[4]
			method = bVals[5]
			biasB = bVals[6]
			scaleB = bVals[7]
			bias = bVals[8]
			scale = bVals[9]
			#Var for storing differents CCC
			ccc = []
			print(v.goodColor+"Test prediction in progress..."+v.endColor)
			#Concatenation of ARFF data
			concRec(wSize, wStep, nMod)
			#Normalisation of Features
			normFeatures(wSize, wStep, nMod)
			#We open the files for the unimodal prediction
			[tr,de, te] = unimodalPredPrep(wSize, wStep, nMod)
			#We open the files for the Gold Standard Matching
			[art, vat, dt] = gsOpen(wSize,wStep, True, nMod)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(method, dl, wSize, wStep, art, vat, dt, True)
			#We do the prediction on Dev/Test
			[cccTest, predTest, cccDev, predDev] = unimodalPredTest(gs, c, tr, te, de, nDim)
			#Post-treatement
			[cccTest, cccDev] = postTreatTest(gs, predTest, cccTest, predDev, cccDev, bias, scale, biasB, scaleB, nDim)
			#We store the results
			ccc = [nDim, round(cccDev,2), round(cccTest,2), round(wSize,2), round(wStep,2), round(dl,2), c, method, biasB, scaleB, bias, scale]
			printValTest(ccc)
#End predictTest
