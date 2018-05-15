#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from ConcArff import concGs, concRec
from FeatsNorm import normFeatures
from PostTreats import postTreatTest
from PredUtils import unimodalPredPrep, cccCalc, cutTab, predMulti
from Print import printValTest
from GSMatching import gsOpen, gsMatch
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict
from sklearn import linear_model
import numpy as np
import scipy as sp
import timeit
import cPickle

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
	return cccTest, predTest, cccDev, predDev, gsDe, gsTe
#Fin unimodalPredictionDev

#Predict on test the best values found with Dev and print the results
def predictTest():
	bestVals=cPickle.load(open("../Pred/BestValues.txt"))
	#Concatenation of Gold Standards
	concGs(True)
	#Tab for the linear regression
	predictionsDev = []
	predictionsTest = []
	gsDev = []
	gsTest = []
	for nDim in range(len(v.eName)):
		predictionsDev.append([])
		predictionsTest.append([])
		gsDev.append([])
		gsTest.append([])
	for nMod in range(len(v.desc)):
		for nDim in range(len(v.eName)):
			bVals = bestVals[v.nameMod[nMod]][nDim]
			#Value/wSize/wStep/Delay/Complexity/BiasUse/ScaleUse/BiasValue/ScaleValue
			wSize = float(bVals[1])
			wStep = float(bVals[2])
			dl = float(bVals[3])
			c = float(bVals[4])
			method = str(bVals[5])
			biasB = bVals[6]
			scaleB = bVals[7]
			bias = float(bVals[8])
			scale = float(bVals[9])
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
			[art, vat, dt] = gsOpen(wSize, True, nMod)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(method, dl, wSize, art, vat, dt, True)
			#We do the prediction on Dev/Test
			[cccTest, predTest, cccDev, predDev, gsDe, gsTe] = unimodalPredTest(gs, c, tr, te, de, nDim)
			if (len(gsDev[nDim]) > len(gsDe) or len(gsDev[nDim]) == 0):
				gsDev[nDim] = gsDe
			if (len(gsTest[nDim]) > len(gsTe) or len(gsTest[nDim]) == 0):
				gsTest[nDim] = gsTe
			#Post-treatement
			[cccTest, cccDev, predDev, predTest] = postTreatTest(gs, predTest, cccTest, predDev, cccDev, bias, scale, biasB, scaleB, nDim)
			predictionsDev[nDim].append(predDev)
			predictionsTest[nDim].append(predTest)
			#We store the results
			ccc = [nDim, round(cccDev,2), round(cccTest,2), round(wSize,2), round(wStep,2), round(dl,2), c, method, biasB, scaleB, bias, scale]
			printValTest(ccc,nMod)
	#We fix the size of the tab of prediction
	predictionsDev = cutTab(predictionsDev)
	predictionsTest = cutTab(predictionsTest)
	#Now we do the linear regression
	for nDim in range(len(v.eName)):
		#Getting the coefficient for each modality on Dev
		reg = linear_model.LinearRegression()
		reg.fit(np.transpose(predictionsDev[nDim]),np.array(gsDev[nDim]))
		coef = reg.coef_
		print ("The coefficients for each modality are : "+str(coef))
		#Doing the new prediction
		predM = predMulti(coef,predictionsDev[nDim])
		print cccCalc(predM,gsDev[nDim])
#End predictTest
