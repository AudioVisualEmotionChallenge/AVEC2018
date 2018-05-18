#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from PredUtils import cutTab, predMulti, cccCalc
from GSMatching import gsOpen, gsMatch
sys.path.append(v.labLinearPath)
from sklearn import linear_model
import numpy as np

#Do the linear regression and store results for each function tested
def linearRegression(preds, gs):
	res = []
	#We fix the size of the tab of prediction
	for s in v.aPart:
		preds[s] = cutTab(preds[s])
		gs[s] = np.array(gs[s])
	#We test functions and store results
	for nbFunc in range(len(v.lFunc)):
		for c in v.parFunc[nbFunc]:
			func = v.lFunc[nbFunc][0]
			funcType = v.lFunc[nbFunc][1]
			if (funcType == 0):
				res.append(linearRegressionMono(preds, gs, func, c))
			else :
				res.append(linearRegressionMult(preds, gs, func, c))
	return res

#Do the multimodal unidimensional linear regression and store the results
def linearRegressionMono(preds, gs, func, c):
	res = [func,c]
	coef = []
	cccs = []
	#Now we do the linear regression
	for nDim in range(len(v.eName)):
		#Getting the coefficient for each modality on Dev
		if (c != 0):
			reg = func(alpha=c)
		else :
			reg = func()
		reg.fit(np.transpose(preds['dev'][nDim]),gs['dev'][:,nDim])
		coef.append(reg.coef_)
		#Doing the new prediction
		predM = {}
		ccc = []
		for s in v.aPart :
			predM[s] = predMulti(coef[nDim],preds[s],nDim,0)
			ccc.append(round(cccCalc(predM[s],gs[s][:,nDim]),3))
		cccs.append(ccc)
	res.append(coef)
	res.append(cccs)
	return res
#End linearRegression

#Do the multimodal multidimentionnal linear regression and print the results
def linearRegressionMult(preds, gs, func, c):
	res = [func,c]
	#Getting the coefficient for each modality on Dev
	if (c != 0):
		reg = func(alpha=c)
	else :
		reg = func()
	arou = np.transpose(preds['dev'][0])
	val = np.transpose(preds['dev'][1])
	reg.fit(np.concatenate((arou,val),axis=1),gs['dev'])
	res.append(reg.coef_)
	#Doing the new prediction
	predM = {}
	cccs = []
	for nDim in range(len(v.eName)):
		ccc = []
		for s in v.aPart :
			predM[s] = predMulti(reg.coef_,preds[s],nDim,1)	
			ccc.append(round(cccCalc(predM[s],gs[s][:,nDim]),3))
		cccs.append(ccc)
	res.append(cccs)
	return res
#End linearRegression
