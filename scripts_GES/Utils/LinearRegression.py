#Author: Adrien Michaud
import sys
import numpy as np
import copy
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from PredUtils import cutTabs, predMulti, cccCalc
from GSMatching import gsOpen, gsMatch
from Print import bestLinearRegression, CSVtab
sys.path.append(v.labLinearPath)
from sklearn import linear_model

#Do the linear regression and store results for each function tested
def linearRegression(datas, part):
	res = []
	#We test functions and store results
	for nbFunc in range(len(v.lFunc)):
		res.append([])
		for c in v.parFunc[nbFunc]:
			func = v.lFunc[nbFunc]
			if (func[1] == 0):
				res[nbFunc].append(linRegMono(datas, func, c, part))
			else :
				res[nbFunc].append(linRegMult(datas, func, c, part))
	return res

#Do the multimodal unidimensional linear regression and store the results
def linRegMono(datas, func, c, part):
	res = [func,c,[],[],{}]
	#Now we do the linear regression
	for nDim in range(len(v.eName)):
		#Getting the coefficient for each modality on Dev
		if (c != 0):
			reg = func[0](alpha=c)
		else :
			reg = func[0]()
		reg.fit(np.transpose(datas['dev'][nDim]),datas['gsdev'][nDim])
		res[2].append(reg.coef_)
		#Doing the new prediction
		cccs = []
		for s in part :
			if (res[4].get(s,None) == None):
				res[4][s] = []
			res[4][s].append(predMulti(res[2][nDim],datas[s],nDim,0))
			cccs.append(round(cccCalc(res[4][s][nDim],datas['gs'+s][nDim]),3))
		res[3].append(cccs)
	return res
#End linRegMono

#Do the multimodal multidimentionnal linear regression and print the results
def linRegMult(datas, func, c, part):
	res = [func,c,[],[],{}]
	#Getting the coefficient for each modality on Dev
	if (c != 0):
		reg = func[0](alpha=c)
	else :
		reg = func[0]()
	concPreds = np.concatenate((np.transpose(datas['dev'][0]),np.transpose(datas['dev'][1])),axis=1)
	reg.fit(concPreds,np.transpose(datas['gsdev']))
	res[2] = reg.coef_
	#Doing the new prediction
	cccs = []
	for nDim in range(len(v.eName)):
		cccs = []
		for s in part :
			if (res[4].get(s,None) == None):
				res[4][s] = []
			res[4][s].append(predMulti(reg.coef_,datas[s],nDim,1))
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
	#We get the context
	datas = takeContext(datas, part)
	#Multimodal hierachic representation, we use all modality
	datasC = copy.deepcopy(datas)
	print ("Multimodal hierarchic : ")
	linReg = linearRegression(datasC, part)
	bLinReg = bestLinearRegression(linReg, v.nameMod, part, datas)
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
	for s in 'gstrain','gsdev','gstest','cccs':
		datasM[s] = copy.deepcopy(datas[s])
	#Fusion of the multi representative way
	print("Multirepresentative :")
	multReg = linearRegression(datasM, part)
	bMultReg = bestLinearRegression(multReg,v.catMod, part, datasM)
	#Write the csv with results
	CSVtab(datas,linReg, bLinReg, catReg, bCatReg, multReg, bMultReg, part)
