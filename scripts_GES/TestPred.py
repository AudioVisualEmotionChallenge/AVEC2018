import GlobalsVars as v
from ConcArff import concGs, concRec
from AudioPred import unimodalPredPrep, unimodalPredTest
from Print import printValTest
from GSMatching import gsOpen, gsMatch
from FeatsNorm import normFeatures
from PostTreats import postTreatTest
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import scipy as sp
from scipy import signal
sys.path.append(v.labLinearPath)
import timeit

#Predict on test the best values found with Dev and print the results
def predictTest():
	for nDim in range(len(v.bAudio)):
		#Value/wSize/wStep/Delay/Complexity/MedianFilter/MethodMatching/BiasUse/ScaleUse/BiasValue/ScaleValue
		wSize = v.bAudio[nDim][1]
		wStep = v.bAudio[nDim][2]
		dl = v.bAudio[nDim][3]
		c = v.bAudio[nDim][4]
		medF = v.bAudio[nDim][5]
		method = v.bAudio[nDim][6]
		biasB = v.bAudio[nDim][7]
		scaleB = v.bAudio[nDim][8]
		bias = v.bAudio[nDim][9]
		scale = v.bAudio[nDim][10]
		#Var for storing differents CCC
		ccc = []
		#Concatenation of Gold Standards
		concGs()
		print(v.goodColor+"Test prediction in progress..."+v.endColor)
		#Concatenation of ARFF data
		concRec(wSize, wStep)
		#Normalisation of Features
		normFeatures(wSize, wStep)
		#We open the files for the unimodal prediction
		[tr,de, te] = unimodalPredPrep(wSize, wStep)
		#We open the files for the Gold Standard Matching
		[art, vat, dt] = gsOpen(wSize,wStep)
		#We matche GoldStandards with parameters(wStep/fsize) and stock them
		gs = gsMatch(method, dl, wSize, wStep, art, vat, dt)
		#We do the prediction
		[cccTest, pred] = unimodalPredTest(gs, c, tr, te, medF, nDim)
		#Post-treatement
		cccSave = postTreatTest(pred, gs, cccTest, bias, scale, biasB, scaleB, nDim)
		#We store the results
		ccc = [nDim, round(cccSave,2), round(wSize,2), round(wStep,2), round(dl,2), c, medF, method, biasB, scaleB, bias, scale]
		printValTest(ccc)
#End predictTest
