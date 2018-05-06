import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from ConcArff import concGs, concRec
from GSMatching import gsOpen, gsMatch
from FeatsNorm import normFeatures
from PostTreats import postTreatDev
from PredUtils import unimodalPredPrep, cccCalc
sys.path.append("../AudioPred/")
from AudioPred import unimodalPredDev, bestdelay, earlyStopDelay
from Setup import setup
from GSMatching import gsMatch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import signal

#Test function to print the granularity of gold standards
def printGoldStandard():
	tfenetre = v.sizeBeg
	while (tfenetre <= v.sizeMax) :
		fstep = v.stepBeg
		while (fstep < float(tfenetre)) :
			dl = 0
			gs = goldStandardMatch(v.matchGS, dl, tfenetre, fstep)
			#We print the granularity
			plt.plot(np.array(gs['train_ind']),np.array(gs['train'])[:,0])
			fstep += v.stepStep
		tfenetre += v.sizeStep
		plt.show()
#printGoldStandard

#Test function to print the gold standards for each delay
def printGoldStandardDel():
	tfenetre = v.sizeBeg
	while (tfenetre <= v.sizeMax) :
		fstep = v.stepBeg
		while (fstep < float(tfenetre)) :
			dl = 0
			while (dl <= fstep):
				gs = goldStandardMatch(v.matchGS, dl, tfenetre, fstep)
				#We print the granularity
				plt.plot(np.array(gs['train_ind']),np.array(gs['train'])[:,0])
				dl += v.delStep
			plt.show()
			fstep += v.stepStep
		tfenetre += v.sizeStep
#End printGoldStandardDel

def printPerfOneSizeDel():
	ccc = []
	tab = []
	plttab = []
	wSize = 6.0
	wStep = 1.6
	print(v.goodColor+"Unimodal prediction in progress : "+str(wSize)+"/"+str(wStep)+"..."+v.endColor)
	concRec(wSize, wStep)
	normFeatures(wSize,wStep)
	delay = v.delBeg
	earlystop = [3,3]
	bDmU = [None,None]
	bD = [None,None]
	[tr,de, te] = unimodalPredPrep(wSize, wStep)
	[art, vat, dt] = gsOpen(wSize,wStep, False)
	while (delay <= v.delMax):
		gs = gsMatch(v.matchGS[0], delay, wSize, wStep, art, vat, dt, False)
		for comp in range(len(v.C)):
			[cccDev, pred] = unimodalPredDev(gs, v.C[comp], tr, de, earlystop)
			[cccSave, biasB, scaleB, bias, scale] = postTreatDev(cccDev, pred, gs, earlystop)
			ccc.append([wSize, wStep, round(cccSave[0],2), round(cccSave[1],2), round(delay,2), comp])
		bDelay = bestdelay(round(ccc,2), round(wSize,2), round(wStep,2), round(delay,2))
		tab.append(bDelay)
		plttab.append(delay)
		if (earlyStopDelay(earlystop, bDmU, bD, bDelay)) :
			print ("Earlystopping active pour le delay : "+str(delay)+ " avec meilleur delay a : "+str(bDelay))
			break
		delay += v.delStep
	print(v.goodColor+"Unimodal prediction finished : window size:"+str(wSize)+" window step:"+str(wStep)+v.endColor)
	plt.plot(plttab,np.array(tab)[:,0])
	print plttab, np.array(tab)[:,0]
	plt.show()
	plt.plot(plttab,np.array(tab)[:,1])
	print plttab, np.array(tab)[:,1]
	plt.show()

def main():
	setup()
	printPerfOneSizeDel()

main()
