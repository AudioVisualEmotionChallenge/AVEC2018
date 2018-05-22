#Author: Adrien Michaud
import sys
import numpy as np
import copy
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from PredUtils import cutTab, predMulti, cccCalc
from GSMatching import gsOpen, gsMatch
from Print import bestLinearRegression, CSVtab
sys.path.append(v.labLinearPath)
from sklearn import linear_model

#Do the linear regression and store results for each function tested
def linearRegression(preds, gs, part):
	res = []
	#We test functions and store results
	for nbFunc in range(len(v.lFunc)):
		res.append([])
		for c in v.parFunc[nbFunc]:
			func = v.lFunc[nbFunc]
			if (func[1] == 0):
				res[nbFunc].append(linRegMono(preds, gs, func, c, part))
			else :
				res[nbFunc].append(linRegMult(preds, gs, func, c, part))
	return res

#Do the multimodal unidimensional linear regression and store the results
def linRegMono(preds, gs, func, c, part):
	res = [func,c]
	coef = []
	cccs = []
	predM = {}
	#Now we do the linear regression
	for nDim in range(len(v.eName)):
		#Getting the coefficient for each modality on Dev
		if (c != 0):
			reg = func[0](alpha=c)
		else :
			reg = func[0]()
		print len(np.transpose(preds['dev'][nDim])),len(gs[nDim])
		reg.fit(np.transpose(preds['dev'][nDim]),gs[nDim])
		coef.append(reg.coef_)
		#Doing the new prediction
		ccc = []
		for s in part :
			if (predM.get(s,None) == None):
				predM[s] = []
			predM[s].append(predMulti(coef[nDim],preds[s],nDim,0))
			ccc.append(round(cccCalc(predM[s][nDim],gs[nDim]),3))
		cccs.append(ccc)
	res.append(coef)
	res.append(cccs)
	res.append(predM)
	return res
#End linRegMono

#Do the multimodal multidimentionnal linear regression and print the results
def linRegMult(preds, gs, func, c, part):
	res = [func,c]
	#Getting the coefficient for each modality on Dev
	if (c != 0):
		reg = func[0](alpha=c)
	else :
		reg = func[0]()
	reg.fit(np.concatenate((np.transpose(preds['dev'][0]),np.transpose(preds['dev'][1])),axis=1),gs)
	res.append(reg.coef_)
	#Doing the new prediction
	predM = {}
	cccs = []
	for nDim in range(len(v.eName)):
		ccc = []
		for s in part :
			if (predM.get(s,None) == None):
				predM[s] = []
			predM[s].append(predMulti(reg.coef_,preds[s],nDim,1))
			ccc.append(round(cccCalc(predM[s][nDim],gs[nDim]),3))
		cccs.append(ccc)
	res.append(cccs)
	res.append(predM)
	return res
#End linRegMult

def regression(datas, modeTest):
	if (modeTest == True):
		part = ['dev','test']
	else :
		part = ['dev']
	#We fix the size of the tab of prediction
	for s in part:
		datas[s] = cutTab(datas[s])
		datas['gs'] = np.array(datas['gs'])
	#Multimodal hierachic representation, we use all modality
	linPreds = {}
	for s in part:
		linPreds[s] = copy.deepcopy(datas[s])
	linGs = copy.deepcopy(datas['gs'])
	linReg = linearRegression(linPreds, linGs, part)
	bestLinearRegression(linReg, v.nameMod, part)
	#Multireprensentative, we do it for each category of modality
	catReg = []
	multPreds = {}
	for nCat in range(len(v.catMod)):
		catGs = copy.deepcopy(datas['gs'])
		catPreds = {}
		for s in part:
			catPreds[s] = copy.deepcopy(datas[s])
		#We take the sample of the category out from preds
		for s in part:
			for nDim in range(len(v.eName)):
				for nMod in reversed(range(len(v.nameMod))):
					if (v.nameMod[nMod] not in v.catModApp[nCat]):
						del(catPreds[s][nDim][nMod])
						nMod -= 1
		catReg.append(linearRegression(catPreds, catGs, part))
		r =  bestLinearRegression(catReg[nCat],v.catModApp[nCat], part)
		for s in part:
			if (multPreds.get(s,None) == None):
				multPreds[s]=[]
				for nDim in range(len(v.eName)):
					multPreds[s].append([])
			for nDim in range(len(v.eName)):
				multPreds[s][nDim].append(r[s][nDim])
	#Fusion of the multi representative way
	multGs = copy.deepcopy(datas['gs'])
	multReg = linearRegression(multPreds, multGs, part)
	bestLinearRegression(multReg,v.catMod, part)
	CSVtab(datas['cccs'],linReg, catReg, multReg, part)
