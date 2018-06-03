#Author: Adrien Michaud
import sys
import numpy as np
import copy
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from PredUtils import cutTabs, predMulti, cccCalc, tabContext
from GSMatching import gsOpen, gsMatch
from Print import bestLinearRegression, CSVtab
sys.path.append(v.labLinearPath)
from sklearn import linear_model

#Do the linear regression and store results for each function tested
def linearRegression(datas, part):
	res = []
	for nbFunc in range(len(v.lFunc)):
		res.append([])
	#We test each combinaise of contexts
	for cMode in v.cModes:
		for cSize in v.cSizes:
			#We need to increase the context
			datasCont = copy.deepcopy(datas)
			for s in part:
				for nDim in range(len(v.eName)):
					for nMod in range(len(datas[s][nDim])):
						datasCont[s][nDim][nMod] = tabContext(datas[s][nDim][nMod],cMode,cSize)
			#We test functions and store results
			for nbFunc in range(len(v.lFunc)):
				for c in v.parFunc[nbFunc]:
					func = v.lFunc[nbFunc]
					if (func[1] == 0):
						res[nbFunc].append(linRegMono(datasCont, func, c, part, cMode, cSize))
					else :
						res[nbFunc].append(linRegMult(datasCont, func, c, part, cMode, cSize))
	return res

#Do the multimodal unidimensional linear regression and store the results
def linRegMono(datas, func, c, part, cMode, cSize):
	res = [func,c,[],[],{}, cMode, cSize]
	#Now we do the linear regression
	for nDim in range(len(v.eName)):
		#Getting the coefficient for each modality on Dev
		if (c != 0):
			reg = func[0](alpha=c)
		else :
			reg = func[0]()
		for nMod in range(len(datas['dev'][nDim])):
			if (nMod == 0):
				preds = datas['dev'][nDim][nMod]
			else :
				preds = np.concatenate((preds,datas['dev'][nDim][nMod]),axis=1)
		reg.fit(preds,datas['gsdev'][nDim])
		res[2].append(reg.coef_)
		#Doing the new prediction
		cccs = []
		for s in part :
			if (res[4].get(s,None) == None):
				res[4][s] = []
			pred = predMulti(res[2][nDim],datas[s],nDim,0, cSize)
			res[4][s].append(pred)
			cccs.append(round(cccCalc(pred,datas['gs'+s][nDim]),3))
		res[3].append(cccs)
	return res
#End linRegMono

#Do the multimodal multidimentionnal linear regression and print the results
def linRegMult(datas, func, c, part, cMode, cSize):
	res = [func,c,[],[],{}, cMode, cSize]
	#Getting the coefficient for each modality on Dev
	if (c != 0):
		reg = func[0](alpha=c)
	else :
		reg = func[0]()
	for nDim in range(len(v.eName)):
		for nMod in range(len(datas['dev'][nDim])):
			if (nMod == 0):
				preds = datas['dev'][nDim][nMod]
			else :
				preds = np.concatenate((preds,datas['dev'][nDim][nMod]),axis=1)
	reg.fit(preds,np.transpose(datas['gsdev']))
	res[2] = reg.coef_
	#Doing the new prediction
	cccs = []
	for nDim in range(len(v.eName)):
		cccs = []
		for s in part :
			if (res[4].get(s,None) == None):
				res[4][s] = []
			res[4][s].append(predMulti(reg.coef_,datas[s],nDim,1, cSize))
			cccs.append(round(cccCalc(res[4][s][nDim],datas['gs'+s][nDim]),3))
		res[3].append(cccs)
	return res
#End linRegMult

def regression(datas, modeTest):
	if (modeTest == True):
		part = ['dev','test']
	else :
		part = ['dev']
	#We fix the size of the tab of prediction
	datas = cutTabs(datas, part)
	#Multimodal hierachic representation, we use all modality
	datasC = copy.deepcopy(datas)
	print ("Multimodal hierarchic : ")
	linReg = linearRegression(datasC, part)
	bLinReg = bestLinearRegression(linReg, v.nameMod, part, datasC)
	#Multireprensentative, we do it for each category of modality
	print ("Multimodal representative : ")
	catReg = []
	bCatReg = []
	datasM = {}
	for nCat in range(len(v.catMod)):
		dataCat = copy.deepcopy(datas)
		#We take the sample of the category out from preds
		for nDim in range(len(v.eName)):
			for nMod in reversed(range(len(v.nameMod))):
				if (v.nameMod[nMod] not in v.catModApp[nCat]):
					for s in part:
						del(dataCat[s][nDim][nMod])
					del(dataCat['cccs'][nDim][nMod])
					nMod -= 1
		catReg.append(linearRegression(dataCat, part))
		print("Category : "+v.catMod[nCat])
		bCatReg.append(bestLinearRegression(catReg[nCat],v.catModApp[nCat], part, dataCat))
		for s in part:
			if (datasM.get(s,None) == None):
				datasM[s]=[]
				for nDim in range(len(v.eName)):
					datasM[s].append([])
			for nDim in range(len(v.eName)):
				datasM[s][nDim].append(bCatReg[nCat][s][nDim][0])
		if (datasM.get('cccs',None) == None):
			datasM['cccs']=[]
			for nDim in range(len(v.eName)):
				datasM['cccs'].append([])
				datasM['cccs'][nDim].append(bCatReg[nCat]['dev'][nDim][2])
	for s in 'gstrain','gsdev','gstest':
		datasM[s] = copy.deepcopy(datas[s])
	#Fusion of the multi representative way
	print("Multirepresentative :")
	multReg = linearRegression(datasM, part)
	bMultReg = bestLinearRegression(multReg,v.catMod, part, datasM)
	#Write the csv with results
	CSVtab(datas,linReg, bLinReg, catReg, bCatReg, multReg, bMultReg, part)
