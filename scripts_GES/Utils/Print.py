#Author: Adrien Michaud
import GlobalsVars as v
import numpy as np
from PredUtils import restaurObject, saveObject
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def CSVtab(cccs, linReg, catReg, multReg, part):
	#Tab for unimodal CCC
	#Labels
	tabCCC = "Unimodal"
	for nMod in range(len(v.desc)):
		tabCCC += ";"+v.nameMod[nMod]
	tabCCC += "\n"
	#Data
	for nDim in range(v.nDim):
		for nPart in range(len(part)):
			tabCCC+= v.eName[nDim]+" - "+part[nPart]
			for nMod in range(len(v.desc)):
				tabCCC += ";"+str(cccs[nDim][nMod][0][nPart])
			tabCCC += "\n"
	tabCCC += "\n"
	#Tab for multimodal - multi representative
	#Labels
	tabCCC += "Multimodal - Multi-Representation"
	for nFunc in range(len(v.lFunc)):
		tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += "\n"
	#Data
	for nDim in range(v.nDim):
		for nPart in range(len(part)):
			tabCCC += v.eName[nDim]+" - "+part[nPart]
			for nFunc in range(len(v.lFunc)):
				best = bestCCCPartLinRegFunc(linReg,nFunc,nPart,nDim)
				tabCCC += ";"+str(best[3][nDim][nPart])
			tabCCC += "\n"
	tabCCC += "\n"
	#Tab for multirepresentative
	#Labels
	tabCCC += "Multi-Representationel"
	for nCat in range(len(v.catMod)):
		tabCCC += ";"+v.catMod[nCat]
		for nFunc in range(len(v.lFunc)-1):
			tabCCC += ";"
	tabCCC += "\n"
	for nCat in range(len(v.catMod)):
		for nFunc in range(len(v.lFunc)):
			tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += "\n"
	#Data
	for nDim in range(v.nDim):
		for nPart in range(len(part)):
			tabCCC += v.eName[nDim]+" - "+part[nPart]
			for nCat in range(len(v.catMod)):
				for nFunc in range(len(v.lFunc)):
					best = bestCCCPartLinRegFunc(catReg[nCat],nFunc,nPart,nDim)
					tabCCC += ";"+str(best[3][nDim][nPart])
			tabCCC += "\n"
	tabCCC += "\n"
	#Tab for multimodal multirepresentative
	#Labels
	tabCCC += "Multi-modal multi-representation"
	for nFunc in range(len(v.lFunc)):
		tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += "\n"
	#Data
	for nDim in range(v.nDim):
		for nPart in range(len(part)):
			tabCCC += v.eName[nDim]+" - "+part[nPart]
			for nFunc in range(len(v.lFunc)):
				best = bestCCCPartLinRegFunc(multReg,nFunc,nPart,nDim)
				tabCCC += ";"+str(best[3][nDim][nPart])
			tabCCC += "\n"
	tabCCC += "\n"
	#We write the file
	f = open("./results.csv","wb")
	f.write(str(tabCCC))
	f.close()
#End CSVTab
			
#Return the best ccc value for a window size, a window step and a delay given
def bestdelay(cccs, wSize, wStep, delay):
	b = np.zeros(v.nDim)
	for i in range(v.nDim):
		b[i] = -1
	for i in range(len(cccs)):
		for nDim in range(v.nDim):
			if (cccs[i][0] == nDim and round(cccs[i][1],2) == round(wSize,2) and round(cccs[i][2],2) == round(wStep,2) and round(cccs[i][4],2) == round(delay,2) and cccs[i][3] > b[nDim]):
				b[nDim] = cccs[i][3]
	return b	

#Return the best ccc value for a window size and a windows step given
def bestVal(cccs, wSize, wStep):
	b = np.zeros(v.nDim)
	for i in range(v.nDim):
		b[i] = -1
	bD = np.zeros(v.nDim)
	for i in range(len(cccs)):
		for nDim in range(v.nDim):
			if (cccs[i][0] == nDim and round(cccs[i][1],2) == round(wSize,2) and round(cccs[i][2],2) == round(wStep,2) and cccs[i][3] > b[nDim]):
				b[nDim] = cccs[i][3]
				bD[nDim] = cccs[i][4]
	return b, bD

#Get the best CCC for a linear regression function and a partition
def bestCCCPartLinRegFunc(linRegRes, nbFunc, nPart, nDim):
	best = linRegRes[nbFunc][0]
	for i in range(1,len(linRegRes[nbFunc])):
		if (linRegRes[nbFunc][i][3][nDim][nPart] > best[3][nDim][nPart]):
			best = linRegRes[nbFunc][i]
	return best
#End bestCCCPartLinRegFunc

#Get the best CCC for a linear regression and a partition
def bestCCCPartLinReg(linRegRes,nPart, nDim):
	#We get the best ccc for the dimension and partition
	best = bestCCCPartLinRegFunc(linRegRes,0,nPart, nDim)
	for nbFunc in range(len(v.lFunc)):
		res = bestCCCPartLinRegFunc(linRegRes,nbFunc,nPart, nDim)
		if (res[3][nDim][nPart] > best[3][nDim][nPart]):
				best = res
	return best
#End bestCCCPartLinReg

#Get the best results and print it for the linear regression
def bestLinearRegression(linRegRes, nameMod):
	bestLinReg = {}
	for nDim in range(len(v.eName)):
		for nPart in range(len(v.aPart)):
			best = bestCCCPartLinReg(linRegRes,nPart, nDim)
			if (bestLinReg.get(v.aPart[nPart],None) == None):
				bestLinReg[v.aPart[nPart]] = []
			bestLinReg[v.aPart[nPart]].append(best[4][v.aPart[nPart]][nDim])
			#We print it
			print ("Best linear regression for "+v.eName[nDim]+" on "+v.aPart[nPart]+" : "+str(best[3][nDim][nPart]))
			if (v.debugMode == True):
				print ("With func/complexity : "+str(best[0][2])+"/"+str(best[1]))
				print ("Modality : Coefficient")
				if (best[0][1] == 0):
					for nMod in range(len(best[2][nDim])):
						print(nameMod[nMod]+" : "+str(round(best[2][nDim][nMod],3)))
				else :
					for nDim in range(len(v.eName)):
						lenNMod = len(best[2][nDim])/2
						for nMod in range(lenNMod):
							print(v.eName[nDim][0:1]+" "+nameMod[nMod]+" : "+str(round(best[2][nDim][nMod+nDim*lenNMod],3)))
			print("")
	return bestLinReg
#End bestLinearRegression

#Print the CCC value and parameters
def printValTest(cccs, nMod, nDim):
	ccc = cccs[nMod][nDim]
	print(v.eName[nDim]+"/"+v.nameMod[nMod])
	print("Value Dev/Test : "+str(ccc[0][0])+"/"+str(ccc[0][1]))
	if (v.debugMode == True):
		print("Window size/step/delay/complexity : "+str(ccc[1])+"/"+str(ccc[2])+"/"+str(ccc[3])+"/"+str(ccc[4]))
		print("Bias/Scaling : "+str(ccc[5])+"/"+str(ccc[6]))
	print("")
#End printValue	

#Print the best CCC values
def printBestVal(cccs, tPlt, nMod):
	#We take the best values
	cccs = np.array(cccs)
	tPlt = np.array(tPlt)
	bVals = []
	for nDim in range(v.nDim):
		bVal = cccs[0]
		for i in range(1,len(cccs)):
			if (cccs[i][0] == nDim and cccs[i][3] > bVal[3]):
				bVal = cccs[i]
		#We print the results
		print("Best value : "+v.nameMod[nMod]+" "+v.eName[nDim]+" : "+str(bVal[3]))
		bVals.append(bVal)
		if (v.debugMode == True):
			print("Window size/step/delay/complexity : "+str(bVal[1])+"/"+str(bVal[2])+"/"+str(bVal[4])+"/"+str(bVal[5]))
			print("Bias/Scaling "+v.eName[nDim]+" : "+str(bVal[6])+"/"+str(bVal[7]))
		print("")
		#We print it in graphical form
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(tPlt[:,0], tPlt[:,1], tPlt[:,2+nDim])
		#Labels for axes
		ax.set_xlabel("Window Size")
		ax.set_ylabel("Window Step")
		ax.set_zlabel(v.nameMod[nMod]+" : CCC for "+v.eName[nDim])
		#We save the plot
		f = open("../Figures/"+v.nameMod[nMod]+"_"+v.eName[nDim]+".png","wb")
		plt.savefig(f)
	val = restaurObject("./BestValues.obj")
	val[v.nameMod[nMod]] = bVals
	saveObject(val,"./BestValues.obj")
#End printBestValues
