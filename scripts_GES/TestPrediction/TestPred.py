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
	for s in 'dev','test':
		pred[s] = np.array(predict(gsu[s],feat[s],model,"-q"))[0]
		#We calculate the correlation and store it
		ccc[s] = cccCalc(np.array(pred[s]),gsu[s])
	return ccc, pred, gsu
#Fin unimodalPredictionDev

#Print the best results for the unidimensionnal linear regression
def bestLinearRegressionMono(results):
	for nDim in range(len(v.eName)):
		for a in range(len(v.aPart)):
			#We get the best ccc for the dimension and partition
			best = results[0]
			for i in range(1,len(results)):
				if (results[i][4+a] > best[4+a]):
					best = result[i]
			#We print it
			print best
			print ("The best linear regression for "+best[0])
			print ("With func/complexity : "+str(best[1])+"/"+str(best[2]))
			print ("The coefficients for each modality are : ")
			for nMod in range(len(v.desc)):
				print(v.nameMod[nMod]+" : "+str(best[3][nMod]))
			print ("With ccc dev/test "+str(best[4])+"/"+str(best[5]))
#End bestLinearRegressionMono

#Do the multimodal linear regression and print the results
def linearRegressionMono(preds, gsa):
	results = []
	#We fix the size of the tab of prediction
	for s in v.aPart:
		preds[s] = cutTab(preds[s])
	#For all the functions used
	for nbFunc in range(len(lFunc)):
		for param in range(len(parFunc[nbFunc])):
			for c in param :
				#Now we do the linear regression
				for nDim in range(len(v.eName)):
					func = lFunc[nbFunc][0]
					funcType = lFunc[nbFunc][1]
					res = [v.eName[nDim],func,c]
					#Getting the coefficient for each modality on Dev
					if (c != 0):
						reg = func(alpha=c)
					else :
						reg = func()
					if (funcType == 0):
						reg.fit(np.transpose(preds['dev'][nDim]),np.array(gsa['dev'][nDim]))
						res.append(reg.coef_)
						coef = reg.coef_
					else:
						reg.fit(np.transpose(preds['dev']),np.array(gsa['dev']))
						res.append(reg.coef_[nDim])
						coef = reg.coef_[nDim]
					#Doing the new prediction
					predM = {}
					for s in v.aPart :
						predM[s] = predMulti(coef,preds[s][nDim])	
						res.append(round(cccCalc(predM[s],gsa[s][nDim]),3))
					results.append(res)
	return results
#End linearRegression

#Predict on test the best values found with Dev and print the results
def predictTest():
	bestVals=cPickle.load(open("../Pred/BestValues.txt"))
	#Concatenation of Gold Standards
	concGs(True)
	#Tab for the linear regression
	preds = {}
	gsa = {}
	for s in v.aPart :
		preds[s] = []
		gsa[s] = []
		for nDim in range(len(v.eName)):
			preds[s].append([])
			gsa[s].append([])
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
			feats = unimodalPredPrep(wSize, wStep, nMod)
			#We open the files for the Gold Standard Matching
			gsBase = gsOpen(wSize, True)
			#We matche GoldStandards with parameters(wStep/fsize) and stock them
			gs = gsMatch(method, dl, wSize, gsBase, nMod, True)
			#We do the prediction on Dev/Test
			[ccc, pred, gsu] = unimodalPredTest(gs, c, feats, nDim)
			#Post-treatement
			[ccc, pred] = postTreatTest(gs, pred, ccc, bias, scale, biasB, scaleB, nDim)
			#We save the predictions and GS
			for s in v.aPart :
				if (len(gsa[s][nDim]) > len(gsu[s]) or len(gsa[s][nDim]) == 0):
					gsa[s][nDim] = gsu[s]
				preds[s][nDim].append(pred[s])
			#We store the results
			ccc = [nDim, round(ccc['dev'],2), round(ccc['test'],2), round(wSize,2), round(wStep,2), round(dl,2), c, method, biasB, scaleB, bias, scale]
			printValTest(ccc,nMod)
	#Unidimensionnal
	results = linearRegressionMono(preds, gsa)
	bestLinearRegressionMono(results)
#End predictTest
