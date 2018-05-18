#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
from ConcArff import concGs, concRec
from GSMatching import gsOpen, gsMatch
from FeatsNorm import normFeatures
from PostTreats import postTreatDev
from Print import printBestVal, bestdelay, bestVal
sys.path.append("../Utils/")
from PredUtils import unimodalPredPrep, cccCalc, resamplingTab
from Setup import setup
import operator
import cPickle
import arff
import os
from multiprocessing import Process
import numpy as np
import sys
import scipy as sp
from scipy import signal
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict
import timeit

#Return true if the last three values are not better
def earlyStopDelay(bD, delay, nDim):
	if ((delay-bD[nDim])/v.delStep[nDim] >= v.earlystop) :
		return True
	else :
		return False

#Unimodal prediction on Dev partition
def unimodalPredDev(gs, c, feats, nDim):
	[model, pred, ccc] = [[] for i in range(3)]
	gsDev = np.array(gs['dev'])[:,nDim]
	gsTrain = np.array(gs['train'])[:,nDim]
	#Options for liblinear
	options = "-s "+str(v.sVal)+" -c "+str(c)+" -B 1 -q"
	#We learn the model on train
	model = train(gsTrain,feats['train'],options)
	#We predict on dev data
	pred = predict(gsDev,feats['dev'],model,"-q")[0]
	#We calculate the correlation and store it
	ccc = cccCalc(pred,gsDev)
	return ccc, pred
#Fin unimodalPredictionDev

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def unimodalPred(nMod):
	try:
		#Var for storing differents CCC
		cccs = []
		#Data for the graphic
		tPlt = []
		wSize = v.sizeBeg[nMod]
		while (wSize <= v.sizeMax[nMod]) :
			wStep = v.stepBeg[nMod]
			while (wStep <= v.stepMax[nMod]) :
				print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction in progress : "+str(wSize)+"/"+str(wStep)+"..."+v.endColor)
				#Concatenation of features
				concRec(wSize, wStep, nMod)
				#Normalisation of features
				normFeatures(wSize,wStep, nMod)
				#We open files for the unimodal prediction
				[feats,trainLen] = unimodalPredPrep(wSize, wStep, nMod)
				#We open files for the Gold Standard Matching
				gsBase = gsOpen(wSize, False)
				delay = v.delBeg[nMod]
				while (delay <= v.delMax[nMod]):
					#We match GoldStandards with parameters(wSize, delay) and stock them
					gs = gsMatch(v.matchGS[0], delay, wSize, gsBase, trainLen, False)
					for comp in range(len(v.C)):
						for nDim in range(len(v.eName)):
							#We get the bests CCC value for the wSize/wStep
							b, bD = bestVal(cccs, wSize, wStep)
							if (not earlyStopDelay(bD, delay, nDim)):
								#We do the prediction
								[ccc, pred] = unimodalPredDev(gs, v.C[comp],feats, nDim)
								#Post-treatement
								[ccc, pred, bias, scale] = postTreatDev(ccc, pred, gs, nDim)
								#We store the results
								cccs.append([nDim, round(wSize,2), round(wStep,2), round(ccc,3), round(delay,2), v.C[comp], bias, scale])
					delay += v.delStep[nMod]
				print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction finished : "+str(wSize)+"/"+str(wStep)+v.endColor)
				[b, bD] = bestVal(cccs, wSize, wStep)
				if (v.debugMode == True):
					print(v.nameMod[nMod]+" : Best values for wSize/wStep : "+str(wSize)+"/"+str(wStep)+" Ar/Va "+str(b)+" DlAr/DlVa "+str(bD))
				print("")
				t = [wSize, wStep]
				t.extend(b)
				tPlt.append(t)
				wStep += v.stepStep[nMod]
			wSize += v.sizeStep[nMod]
		printBestVal(cccs, tPlt, nMod)
	except KeyboardInterrupt :
		printBestVal(cccs, tPlt, nMod)
		raise
#End audioPred

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def multimodalPred():
	try :
		bVals = {}
		f = open("./BestValues.txt","wb")
		cPickle.dump(bVals, f)
		f.close()
		ps = []
		pActive = 1
		#For each modality
		print(v.goodColor+"Multimodal prediction in progress..."+v.endColor)
		for nMod in range(len(v.desc)):
			p = Process(target=unimodalPred,args=(nMod,))
			ps.append(p)
			p.start()
			pActive += 1
			while (pActive > v.nThreads):
				for i in range(len(ps)):
					if (not(ps[i].is_alive())):
						ps[i].join()
						pActive -= 1
		#We wait for all processus to end
		for i in range(len(ps)):
			if (ps[i].is_alive()):
				ps[i].join()
	except KeyboardInterrupt:
		for i in range(len(ps)):
			ps[i].terminate()
#End multimodalPred

def Pred(arg):
	#Concatenation of Gold Standards
	concGs(False)
	#UnimodalPred or MultimodalPred
	if (arg == None):
		multimodalPred()
	else :
		unimodalPred(arg)
