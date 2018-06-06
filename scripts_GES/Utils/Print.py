#Author: Adrien Michaud
import GlobalsVars as v
import numpy as np
from PredUtils import restaurObject, saveObject, cccCalc, tabContext
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Print plot for linear regression for comparing context size
def linearRegTab(regRes, name):
	for nDim in range(len(v.eName)):
		b = bestCCCLinReg(regRes, nDim)
		bFunc = 0
		for nbFunc in range(len(v.lFunc)):
			if(b[0][2] == v.lFunc[nbFunc][2]):
				bFunc = nbFunc
		for cMode in v.cModes:
			res = []
			res2 = []
			for cSize in v.cSizes:
				best = -1.0
				for i in range(len(regRes[bFunc])):
					if (regRes[bFunc][i][5] == cMode and regRes[bFunc][i][6] == cSize and regRes[bFunc][i][3][nDim][0] > best):
						best = regRes[bFunc][i][3][nDim][0]
				res.append(best)
				res2.append(round((cSize-1)*0.4,2))
			plt.plot(res2,res, label=cMode,linewidth=0.5, marker='o',linestyle='dashed')
		plt.legend(loc='best')
		plt.ylabel("CCC")
		plt.xlabel("Size of context in seconds")
		f = open("../Figures/plotContext"+name+v.eName[nDim]+v.lFunc[bFunc][2]+".png","wb")
		plt.savefig(f)
		f.close()
		plt.clf()
		print "plt saved"
#End linearRegTab

#Do a CSV containing results
def CSVtab(datas, linReg, bLinReg, catReg, bCatReg, multReg, bMultReg, part):
	cccs = datas['cccs']
	bestVals = []
	for nDim in range(len(v.eName)):
		bestVals.append([])
		for s in range(len(part)):
			bestVals[nDim].append(-1.0)
	#Tab for unimodal CCC
	#Labels
	tabCCC = "Unimodal"
	for nMod in range(len(v.desc)):
		tabCCC += ";"+v.nameMod[nMod]
	tabCCC += "\n"
	#Data
	for nDim in range(len(v.eName)):
		for nPart in range(len(part)):
			s = part[nPart]
			tabCCC+= v.eName[nDim]+" - "+s
			for nMod in range(len(v.desc)):
				tabCCC += ";"+str(cccs[nDim][nMod][0][nPart])+" - "+str(cccs[nDim][nMod][7])+" - "+str(cccs[nDim][nMod][1])+"/"+str(cccs[nDim][nMod][3])
			tabCCC += "\n"
	tabCCC += "\n\n"
	#Tab for multimodal - multi representative
	#Labels
	tabCCC += "Multimodal - Multi-Representative"
	for nFunc in range(len(v.lFunc)):
		tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += ";Best\n"
	#Data
	for nDim in range(len(v.eName)):
		for nPart in range(len(part)):
			s = part[nPart]
			#All functions
			tabCCC += v.eName[nDim]+" - "+s
			for nFunc in range(len(v.lFunc)):
				best = bestCCCLinRegFunc(linReg, nFunc, nDim)
				tabCCC += ";"+str(best[3][nDim][nPart])
			#Best result
			ccc = bLinReg[s][nDim][1]
			if (ccc > bestVals[nDim][nPart]):
					bestVals[nDim][nPart] = round(ccc,3)
			tabCCC += ";"+str(round(ccc,3))+"\n"
	tabCCC += "\n\n"
	#Tab for multirepresentative
	#Labels
	tabCCC += "Multi-Representative"
	for nFunc in range(len(v.lFunc)):
		tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += ";Best\n"
	#Data
	for nCat in range(len(v.catMod)):
		tabCCC += v.catMod[nCat]+"\n"
		for nDim in range(len(v.eName)):
			for nPart in range(len(part)):
				s = part[nPart]
				tabCCC += v.eName[nDim]+" - "+s
				#All functions
				for nFunc in range(len(v.lFunc)):
					best = bestCCCLinRegFunc(catReg[nCat], nFunc, nDim)
					tabCCC += ";"+str(best[3][nDim][nPart])
				#Best result
				ccc = bCatReg[nCat][s][nDim][1]
				tabCCC += ";"+str(round(ccc,3))+"\n"
	tabCCC += "\n\n"
	#Tab for multimodal multirepresentative
	#Labels
	tabCCC += "Multi-modal Hierarchic"
	for nFunc in range(len(v.lFunc)):
		tabCCC += ";"+v.lFunc[nFunc][2]
	tabCCC += ";Best\n"
	#Data
	for nDim in range(len(v.eName)):
		for nPart in range(len(part)):
			s = part[nPart]
			tabCCC += v.eName[nDim]+" - "+s
			#All functions
			for nFunc in range(len(v.lFunc)):
				best = bestCCCLinRegFunc(multReg, nFunc, nDim)
				tabCCC += ";"+str(best[3][nDim][nPart])
			#Best result
			ccc = bMultReg[s][nDim][1]
			if (ccc > bestVals[nDim][nPart]):
					bestVals[nDim][nPart] = round(ccc,3)
			tabCCC += ";"+str(round(ccc,3))+"\n"
	tabCCC += "\n\n"
	#We print the best results
	print("Best results : ")
	for nDim in range(len(v.eName)):
		print v.eName[nDim]+" : ",
		for nPart in range(len(part)):
			print part[nPart]+" : "+str(bestVals[nDim][nPart])+" ",
		print("")
	print("More details in result.csv files")
	#We write the file
	f = open("./results.csv","wb")
	f.write(str(tabCCC))
	f.close()
#End CSVTab
			
#Return the best ccc value for a window size, a window step and a delay given
def bestdelay(cccs, wSize, wStep, delay):
	b = np.zeros(len(v.eName))
	for i in range(len(v.eName)):
		b[i] = -1
	for i in range(len(cccs)):
		for nDim in range(len(v.eName)):
			if (cccs[i][0] == nDim and round(cccs[i][1],2) == round(wSize,2) and round(cccs[i][2],2) == round(wStep,2) and round(cccs[i][4],2) == round(delay,2) and cccs[i][3] > b[nDim]):
				b[nDim] = cccs[i][3]
	return b
#End bestdelay	

#Return the best ccc value for a window size and a windows step given
def bestVal(cccs, wSize, wStep):
	b = np.zeros(len(v.eName))
	for i in range(len(v.eName)):
		b[i] = -1
	bD = np.zeros(len(v.eName))
	for i in range(len(cccs)):
		for nDim in range(len(v.eName)):
			if (cccs[i][0] == nDim and round(cccs[i][1],2) == round(wSize,2) and round(cccs[i][2],2) == round(wStep,2) and cccs[i][3] > b[nDim]):
				b[nDim] = cccs[i][3]
				bD[nDim] = cccs[i][4]
	return b, bD

#Get the best CCC for a linear regression function and a partition
def bestCCCLinRegFunc(linRegRes, nbFunc, nDim):
	best = linRegRes[nbFunc][0]
	for i in range(1,len(linRegRes[nbFunc])):
		if (linRegRes[nbFunc][i][3][nDim][0] > best[3][nDim][0]):
			best = linRegRes[nbFunc][i]
	return best
#End bestCCCPartLinRegFunc

#Get the best CCC for a linear regression and a partition
def bestCCCLinReg(linRegRes, nDim):
	#We get the best ccc for the dimension and partition
	best = bestCCCLinRegFunc(linRegRes,0, nDim)
	for nbFunc in range(1,len(v.lFunc)):
		res = bestCCCLinRegFunc(linRegRes, nbFunc, nDim)
		if (res[3][nDim][0] > best[3][nDim][0]):
			best = res
	return best
#End bestCCCPartLinReg

#Return the best CCC for a dimension and a partition in the cccs tab
def bestDatasCCC(datas, nDim, part):
	bestCCC = []
	for s in range(len(part)):
		bestCCC.append(-1)
	n = 0
	for nMod in range(len(datas['cccs'][nDim])):
		cccs = []
		for nPart in range(len(part)):
			if (datas['cccs'][nDim][nMod] != []):
				cccs.append(round(datas['cccs'][nDim][nMod][0][nPart],3))
		if (cccs != [] and cccs[0] > bestCCC[0]):
			bestCCC = cccs
			n = nMod
	return bestCCC, n
#End bestDatasCCC

#Get the best results and print it for the linear regression
def bestLinearRegression(linRegRes, nameMod, part, datas):
	blr = {}
	for s in part :
		blr[s] = []
	for nDim in range(len(v.eName)):
		best = bestCCCLinReg(linRegRes, nDim)
		[cccs, mod] = bestDatasCCC(datas, nDim, part)
		if (best[3][nDim][0] > cccs[0]):
			for nPart in range(len(part)):
				blr[part[nPart]].append([best[4][part[nPart]][nDim],best[3][nDim][nPart],[]])
			#We print it
			print ("Best linear regression for "+v.eName[nDim]+" : "+str(best[3][nDim]))
			if (v.debugMode == True):
				cMode = best[5]
				cSize = best[6]
				print ("With func/complexity : "+str(best[0][2])+"/"+str(best[1]))
				print ("With context mode/size : "+str(cMode)+"/"+str(cSize))
				print ("Modality : Coefficients")
				if (best[0][1] == 0):
					nombreMod = int(len(best[2][nDim])/cSize)
					for nMod in range(nombreMod):
						print nameMod[nMod]+" : ",
						for size in range(cSize):
							ind = (nMod*cSize)+size
							print str(round(best[2][nDim][ind],3))+ " ",
						print("")
				else :
					for dim in range(len(v.eName)):
						lenNMod = int(len(best[2][nDim])/cSize)
						for nMod in range(lenNMod):
							print v.eName[dim][0:1]+" "+nameMod[nMod]+" : ",
							for size in range(cSize):
								ind = (nMod*cSize)+size
								print str(round(best[2][dim][ind],3))+" ",
							print("")
		else :
			for nPart in range(len(part)):
				blr[part[nPart]].append([datas[part[nPart]][nDim][mod],cccs[nPart],datas['cccs'][nDim][mod]])
			print ("Best linear regression for "+v.eName[nDim]+" : "+str(cccs))
			if (v.debugMode == True):
				print ("Modality : "+nameMod[mod])
		print("")
	return blr
#End bestLinearRegression

#Print the CCC value and parameters
def printValTest(cccs, nMod, nDim):
	ccc = cccs[nDim][nMod]
	print(v.eName[nDim]+"/"+v.nameMod[nMod])
	print("Value Dev/Test : "+str(ccc[0][0])+"/"+str(ccc[0][1]))
	if (v.debugMode == True):
		print("Window size/step/delay : "+str(ccc[1])+"/"+str(ccc[2])+"/"+str(ccc[3]))
		print("Bias/Scaling : "+str(ccc[5])+"/"+str(ccc[6]))
		print("With function/alpha : "+str(ccc[7])+"/"+str(ccc[4]))
	print("")
#End printValue	

#Print the best CCC values
def printBestVal(cccs, tPlt, nMod):
	#We take the best values
	cccs = np.array(cccs)
	tPlt = np.array(tPlt)
	bVals = []
	for nDim in range(len(v.eName)):
		bVal = None
		for i in range(len(cccs)):
			if ((bVal is None and int(cccs[i][0]) == int(nDim)) or (int(cccs[i][0]) == int(nDim) and float(cccs[i][3]) > float(bVal[3]))):
				bVal = cccs[i]
		#We print the results
		if (v.debugMode == True):
			print("Best value : "+v.nameMod[nMod]+" "+v.eName[nDim]+" : "+str(bVal[3]))
			print("Window size/step/delay : "+str(bVal[1])+"/"+str(bVal[2])+"/"+str(bVal[4]))
			print("Bias/Scaling "+v.eName[nDim]+" : "+str(bVal[6])+"/"+str(bVal[7]))
			print("With function/complexity : "+str(bVal[8])+"/"+str(bVal[5]))
		print("")
		bVals.append(bVal)
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
