import sys
sys.path.append("../Config/")
import GlobalsVars as v
from ConcArff import concGs, concRec
from GSMatching import gsOpen, gsMatch
from FeatsNorm import normFeatures
from PostTreats import postTreatDev
from Print import printBestVal
sys.path.append("../Utils/")
from PredUtils import unimodalPredPrep, cccCalc, resamplingTab
from Setup import setup
import operator
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

#Unimodal prediction on Dev partition
def unimodalPredDev(gs, c, tr, de, earlystop):
	[model, pred, cccDev] = [[] for i in range(3)]
	gsC = np.array(gs['dev'])
	#Options for liblinear
	options = "-s "+str(v.sVal)+" -c "+str(c)+" -B 1 -q"
	#[0] = Arousal/[1] = Valence
	for nDim in range(v.nDim):
		if (earlystop[nDim] != 0):
			#We learn the model on train
			model.append(train(np.array(gs['train'])[:,nDim],tr,options))
			#We predict on dev data
			pred.append(predict(gsC[:,nDim],de,model[nDim],"-q")[0])
			#We calculate the correlation and store it
			cccDev.append(cccCalc(np.array(pred[nDim]),gsC[:,nDim]))
		else :
			cccDev.append(-1.0)
			pred.append([])
			model.append(None)
	return cccDev, pred
#Fin unimodalPredictionDev

#Return the best ccc value for a window size, a window step and a delay given
def bestdelay(ccc, wSize, wStep, delay):
	b = np.zeros(v.nDim)
	for i in range(v.nDim):
		b[i] = -1
	for i in range(len(ccc)):
		for nDim in range(v.nDim):
			if (ccc[i][0] == wSize and ccc[i][1] == wStep and ccc[i][4] == delay and ccc[i][2+nDim] > b[nDim]):
				b[nDim] = ccc[i][2+nDim]
	return b	

#Return the best ccc value for a window size and a windows step given
def bestVal(ccc, wSize, wStep):
	b = np.zeros(v.nDim)
	bD = np.zeros(v.nDim)
	for i in range(len(ccc)):
		for nDim in range(v.nDim):
			if (ccc[i][0] == wSize and ccc[i][1] == wStep and ccc[i][2+nDim] > b[nDim]):
				b[nDim] = ccc[i][2+nDim]
				bD[nDim] = ccc[i][4]
	return b, bD

#Return true if the last three best value for delay are decreasing
def earlyStopDelay(earlystop, bDmU, bD, bDelay):
	for nDim in range(v.nDim):
		if (bD[nDim] == None) :
			bD[nDim] = bDelay[nDim]
			bDmU[nDim] = bD[nDim]						
		else :
			if (earlystop[nDim] > 0 and bDelay[nDim] < bD[nDim]):
				earlystop[nDim] -= 1
			elif (earlystop[nDim] > 0 and bDelay[nDim] >= bD[nDim]) :
				earlystop[nDim] = 3
				bDmU[nDim] = bD[nDim]						
				bD[nDim] = bDelay[nDim]
	if (earlystop[0] == 0 and earlystop[1] == 0):
		return True
	else :
		return False

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def unimodalPred(nMod):
	try:
		#Storing the best val here
		bVal = []
		#Var for storing differents CCC
		cccTab = []
		#Data for the graphic
		tPlt = []
		wSize = v.sizeBeg[nMod]
		while (wSize <= v.sizeMax[nMod]) :
			wStep = v.stepBeg[nMod]
			while (wStep <= v.stepMax[nMod]) :
				print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction in progress : "+str(wSize)+"/"+str(wStep)+"..."+v.endColor)
				#Concatenation of ARFF data
				concRec(wSize, wStep, nMod)
				#Normalisation of Features
				normFeatures(wSize,wStep, nMod)
				#We try the delay given as global variables
				delay = v.delBeg[nMod]
				#We prepare the earlystopping for the delays
				earlystop = [3,3]
				bDmU = [None,None]
				bD = [None,None]
				#We open the files for the unimodal prediction
				[tr,de, te] = unimodalPredPrep(wSize, wStep, nMod)
				#We open the files for the Gold Standard Matching
				[art, vat, dt] = gsOpen(wSize, False, nMod)
				while (delay <= v.delMax[nMod]):
					#We match GoldStandards with parameters(wSize, delay) and stock them
					#wStep is always v.tsp for comparison
					gs = gsMatch(v.matchGS[0], delay, wSize, art, vat, dt, False)
					for comp in range(len(v.C)):
						#We do the prediction
						[cccDev, pred] = unimodalPredDev(gs, v.C[comp], tr, de, earlystop)
						#Post-treatement
						[cccSave, biasB, scaleB, bias, scale] = postTreatDev(cccDev, pred, gs, earlystop)
						#We store the results
						cccTab.append([round(wSize,2), round(wStep,2), round(cccSave[0],2), round(cccSave[1],2)
						, round(delay,2), v.C[comp], v.matchGS[0], biasB, scaleB, bias[0], bias[1], scale[0], scale[1]])
					#We get the best CCC for all the delay [0] Arousal/ [1] Valence
					bDelay = bestdelay(cccTab, round(wSize,2), round(wStep,2), round(delay,2))
					#We see if we must earlystop or not
					if (earlyStopDelay(earlystop, bDmU, bD, bDelay)) :
						print (v.nameMod[nMod]+" : Earlystopping active pour le delay : "+str(delay))
						break
					delay += v.delStep[nMod]
				print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction finished : "+str(wSize)+"/"+str(wStep)+v.endColor)
				[b, bD] = bestVal(cccTab, wSize, wStep)
				print(v.nameMod[nMod]+" : Best values for wSize : "+str(wSize)+" wStep : "+str(wStep)+" Ar/Va "+str(b)+" DlAr/DlVa "+str(bD))
				tPlt.append([wSize, wStep, b[0], b[1]])
				#We write in this file for keeping a trace of what we do
				f = open("./cccTab"+v.nameMod[nMod]+".txt","wb").write(str(cccTab))
				wStep += v.stepStep[nMod]
			wSize += v.sizeStep[nMod]
		bVal = printBestVal(cccTab, tPlt, nMod)
		f = open("./BestValues.txt","a").write("\n"+v.nameMod[nMod]+" : "+str(bVal))
	except KeyboardInterrupt :
		printBestVal(cccTab, tPlt, nMod)
		raise
#End audioPred

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def multimodalPred():
	try :
		f = open("./BestValues.txt","wb").write("")
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
