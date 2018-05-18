#Author: Adrien Michaud
import GlobalsVars as v
import numpy as np
import cPickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

#Print the best results for the linear regression
def bestLinearRegression(results):
	for nDim in range(len(v.eName)):
		for a in range(len(v.aPart)):
			#We get the best ccc for the dimension and partition
			best = results[0]
			for i in range(1,len(results)):
				if (results[i][3][nDim] > best[3][nDim]):
					best = results[i]
			#We print it
			print ("The best linear regression for "+v.eName[nDim]+" on "+v.aPart[a]+" : "+str(best[3][nDim][a]))
			if (v.debugMode == True):
				print ("With func/complexity : "+str(best[0])+"/"+str(best[1]))
				print ("Modality : Coefficient")
				if (len(best[2][nDim]) == len(v.desc)):
					for nMod in range(len(v.desc)):
						print(v.nameMod[nMod]+" : "+str(round(best[2][nDim][nMod],3)))
				else :
					for nDim in range(len(v.eName)):
						for nMod in range(len(v.desc)):
							print(v.eName[nDim][0:1]+" "+v.nameMod[nMod]+" : "+str(round(best[2][nDim][nMod+nDim*len(v.desc)],3)))
			print("")
#End bestLinearRegressionMono

#Print the CCC value and parameters
def printValTest(ccc, nMod):
	print(v.eName[ccc[0]]+"/"+v.nameMod[nMod])
	print("Value Dev/Test : "+str(ccc[1])+"/"+str(ccc[2]))
	if (v.debugMode == True):
		print("Window size/step/delay/complexity : "+str(ccc[3])+"/"+str(ccc[4])+"/"+str(ccc[5])+"/"+str(ccc[6]))
		print("Bias/Scaling : "+str(ccc[8])+"/"+str(ccc[9]))
	print("")
#End printValue	

#Print the best CCC values
def printBestVal(cccs, tPlt, nMod):
	#We take the best values
	cccs = np.array(cccs)
	tPlt = np.array(tPlt)
	iMax = np.zeros(v.nDim)
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
	f = open("./BestValues.txt","rb")
	val = cPickle.load(f)
	f.close()
	val[v.nameMod[nMod]] = bVals
	f = open("./BestValues.txt","wb")
	cPickle.dump(val,f)
	f.close()
#End printBestValues
