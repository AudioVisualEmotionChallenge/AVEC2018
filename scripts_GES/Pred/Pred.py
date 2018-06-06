#Author: Adrien Michaud
import sys
import operator
import cPickle
import arff
import multiprocessing
import copy
import warnings
import os
import numpy as np
import sys
import scipy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.append("../Config/")
import GlobalsVars as v
from matplotlib.font_manager import FontProperties
from multiprocessing import Process
from scipy import signal
sys.path.append("../Utils/")
from PredUtils import unimodalPredPrep, cccCalc, cutTab, predMulti, saveObject, restaurObject, initTabData, isInt
from GSMatching import gsOpen, gsMatch
from LinearRegression import regression
from NormConc import normFeatures,concGs, concFeats
from Print import printBestVal, bestdelay, bestVal
from sklearn.exceptions import ConvergenceWarning
from Setup import setup
sys.path.append(v.labLinearPath)
from liblinearutil import train, predict

#Return true if the last three values are not better
def earlyStopDelay(bD, delay, nDim):
	if ((delay-bD[nDim])/v.delStep[nDim] >= v.earlystop) :
		return True
	else :
		return False

#Do the post treatement for dev partition and save if there are better results
def postTreatDev(cccs, preds, gs, nDim):
	#First we calculate the bias
	gsMean = np.nanmean(gs['dev'][nDim])
	predMean = np.nanmean(preds['dev'])
	bias = gsMean - predMean
	#We add the bias to the prediction and save if there is an improvement
	predCenter = preds['dev'] + bias
	cccBias = cccCalc(predCenter,gs['dev'][nDim])
	if (cccBias > cccs['dev']):
		cccs['dev'] = cccBias
		preds['dev'] = predCenter
	else :
		bias = 0.0
	#We now scale the prediction and do the same thing
	#First we calculate the scale
	stdGs = np.nanstd(gs['dev'][nDim])
	stdPred = np.nanstd(preds['dev'])
	scale = stdGs/stdPred
	#We apply the scale and save if improvement
	predScale = np.multiply(preds['dev'],scale)
	cccScale = cccCalc(predScale,gs['dev'][nDim])
	if (cccScale > cccs['dev']) :
		cccs['dev'] = cccScale
		preds['dev'] = predScale
	else :
		scale = 0.0
	return cccs['dev'], preds['dev'], bias, scale
#End postTreatementDev

#Unimodal prediction on partitions
def unimodalPredDev(gs, feats, nDim):
	parts = ['dev']
	[cccs, preds] = [{} for i in range(2)]
	for s in parts:
		cccs[s] = -1.0
	warnings.filterwarnings('ignore', category=ConvergenceWarning)
	#Liblinear
	for comp in v.C:
		#Options for liblinear
		options = "-s "+str(v.sVal)+" -c "+str(comp)+" -B 1 -q"
		#We learn the model on train
		model = train(gs['train'][nDim],feats['train'],options)
		#We predict on data
		for s in parts:
			pred = np.array(predict(gs[s][nDim],feats[s],model,"-q"))[0]
			#We calculate the correlation and store it
			ccc = cccCalc(np.array(pred),gs[s][nDim])
			if (ccc > cccs[s]):
				preds[s] = pred
				cccs[s] = ccc
				function = "SVR"
				alpha = comp
	if (v.fullMode == True):
		#We see if we can do better with sklearn
		for nbFunc in range(len(v.lFunc)):
			for c in v.parFunc[nbFunc]:
				func = v.lFunc[nbFunc]
				reg = func[0](alpha=c)
				#One task prediction
				if (func[1] == 0):
					reg.fit(feats['train'],gs['train'][nDim])
					for s in parts:
						p = reg.predict(feats['dev'])
						ccc = cccCalc(p,gs[s][nDim])
						if (ccc > cccs[s]) : 
							preds[s] = p
							cccs[s] = ccc
							function = func[2]
							alpha = c
				#Multi task prediction
				else :
					reg.fit(feats['train'],np.transpose(gs['train']))
					for s in parts:
						p = reg.predict(feats['dev'])[:,nDim]
						ccc = cccCalc(p,gs[s][nDim])
						if (ccc > cccs[s]) : 
							preds[s] = p
							cccs[s] = ccc
							function = func[2]
							alpha = c
	return cccs, preds, function, alpha
#Fin unimodalPred

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def unimodalPreds(nMod, debugMode, fullMode):
	try:
		v.debugMode = debugMode
		v.fullMode = fullMode
		#Var for storing differents CCC
		res = []
		#Data for the graphic
		tPlt = []
		#Var for storing preds and gs
		data = copy.deepcopy(restaurObject("./datas.obj"))
		wSize = v.sizeBeg[nMod]
		while (wSize <= v.sizeMax[nMod]) :
			wStep = v.stepBeg[nMod]
			while (wStep <= v.stepMax[nMod]) :
				if (v.debugMode == True):
					print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction in progress : "+str(wSize)+"/"+str(wStep)+"..."+v.endColor)
				#Concatenation & normalisation of features
				concFeats(wSize, wStep, nMod)
				normFeatures(wSize,wStep, nMod)
				#We open files for the unimodal prediction
				[feats,trainLen] = unimodalPredPrep(wSize, wStep, nMod)
				delay = v.delBeg[nMod]
				while (delay <= v.delMax[nMod]):
					#We match GoldStandards with parameters(wSize, delay) and stock them
					gs = gsMatch(v.matchGS[1], delay, wSize, nMod, trainLen, False)
					for nDim in range(len(v.eName)):
						[b, bD] = bestVal(res, wSize, wStep)
						if (not earlyStopDelay(bD, delay, nDim)):
							#We do the prediction and post-treatements
							[cccs, preds, function, alpha] = unimodalPredDev(gs, feats, nDim)
							[ccc, pred, bias, scale] = postTreatDev(cccs, preds, gs, nDim)
							#We store the results
							if (len(data['cccs'][nDim][nMod]) == 0 or ccc > data['cccs'][nDim][nMod][0][0]):
								data['dev'][nDim][nMod] = pred
								data['cccs'][nDim][nMod] = [[round(ccc,3)], round(wSize,2), round(wStep,2), round(delay,2), alpha, bias, scale, function]
							if (len(data['gsdev'][nDim]) == 0 or len(data['gsdev'][nDim]) > len(gs['dev'][nDim])):								
								data['gsdev'][nDim] = gs['dev'][nDim]
							res.append([nDim, round(wSize,2), round(wStep,2), round(ccc,3), round(delay,2), alpha, bias, scale, function])
					delay += v.delStep[nMod]
				if (v.debugMode == True):
					print(v.goodColor+v.nameMod[nMod]+" : Unimodal prediction finished : "+str(wSize)+"/"+str(wStep)+v.endColor)
					print(v.nameMod[nMod]+" : Best values for "+str(wSize)+"/"+str(wStep)+" : Ar/Va "+str(b)+" DlAr/DlVa "+str(bD)+"\n")
				t = [wSize, wStep]
				t.extend(b)
				tPlt.append(t)
				wStep += v.stepStep[nMod]
			wSize += v.sizeStep[nMod]
		printBestVal(res, tPlt, nMod)
		datas = restaurObject("./datas.obj")
		for nDim in range(len(v.eName)):
			for s in 'dev','cccs':
				datas[s][nDim][nMod] = data[s][nDim][nMod]
			if (len(datas['gsdev'][nDim]) == 0 or len(datas['gsdev'][nDim]) > len(data['gsdev'][nDim])):
				datas['gsdev'][nDim] = data['gsdev'][nDim]
		saveObject(datas,"./datas.obj")
	except KeyboardInterrupt :
		printBestVal(res, tPlt, nMod)
		raise
#End Pred

#Try all the possibilities given and find the best CCCs values and parameters for each dimensions
def multimodalPreds():
	try :
		ps = []
		pActive = 1
		#For each modality
		print(v.goodColor+"Multimodal prediction in progress..."+v.endColor)
		for nMod in range(len(v.desc)):
			p = Process(target=unimodalPreds,args=(nMod,v.debugMode,v.fullMode))
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
		#We now can do the linear regression
		datas = restaurObject("./datas.obj")
		regression(datas, False)
	except KeyboardInterrupt:
		for i in range(len(ps)):
			ps[i].terminate()
#End multimodalPred

def Pred(arg):
	#Concatenation of Gold Standards
	concGs(False)
	#Creation datas object
	datas = initTabData()
	if (os.path.isfile("./datas.obj") == False):
		saveObject(datas,"./datas.obj")
	#Creation best values object
	bVals = {}
	if (os.path.isfile("./BestValues.obj") != False):
		saveObject(bVals,"./BestValues.obj")
	#UnimodalPred or MultimodalPred
	if (arg == None):
		multimodalPreds()
	else :
		unimodalPreds(arg,v.debugMode,v.fullMode)

def main():
	#These two lines are for windows threads
	if __name__ == '__main__':
		multiprocessing.freeze_support()
		endOrNot = setup(False)
		if (endOrNot == True):
			if (len(sys.argv) > 1) :
				arg = sys.argv[1]
				for i in range(len(sys.argv)):
					if (str(sys.argv[i]) == "--debug" or str(sys.argv[i]) == "debug"):
						v.debugMode = True
					if (str(sys.argv[i]) == "--full" or str(sys.argv[i]) == "full"):
						v.fullMode = True
				if (v.fullMode == True):
					print("Full mode : now doing predictions with linear regression.")
				if (isInt(arg, len(v.desc))):
					Pred(int(arg))
				elif (str(arg) == "help"):
					print("For unimodal prediction, here the correspondance")
					for i in range(len(v.desc)):
						print i,v.nameMod[i]
				elif (str(arg) == "--debug" or str(arg) == "debug" or str(arg) == "full" or str(arg) == "--full"):
					Pred(None)
				else :
					print("Error on arguments")
					print("For unimodal prediction, here the correspondance")
					for i in range(len(v.desc)):
						print i,v.nameMod[i]
					print("For full mode (using linear regressions for predictions) type --full or full")
					print("For debug mode, type --debug or debug")
			else :
				Pred(None)
		else :
			print ("Error on setup, please check files")
main()
