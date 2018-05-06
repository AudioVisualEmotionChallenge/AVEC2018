import GlobalsVars as v
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Print the CCC value and parameters
def printValTest(ccc, nMod):
	print("The values are :")
	print(v.eName[ccc[0]]+"/"+v.nameMod[nMod])
	print("Value Dev/Test : "+str(ccc[1])+"/"+str(ccc[2]))
	print("Window size/step : "+str(ccc[3])+"/"+str(ccc[4]))
	print("Delay/Complexity : "+str(ccc[5])+"/"+str(ccc[6]))
	print("GS method : "+ccc[7])
	print("Use of Bias/Scale : "+str(ccc[8])+"/"+str(ccc[9]))
	print("Bias/Scaling value : "+str(ccc[10])+"/"+str(ccc[11]))
#End printValue	

#Print the best CCC values
def printBestVal(ccc, tPlt, nMod):
	#We take the best values
	ccc = np.array(ccc)
	tPlt = np.array(tPlt)
	iMax = np.zeros(v.nDim)
	for nDim in range(v.nDim):
		bVal = []
		iMax[nDim] = np.where(ccc[:,nDim+2] == max(ccc[:,nDim+2]))[0][0]
		#We print the results
		ind = int(iMax[nDim])
		print("Best values : "+v.nameMod[nMod]+" "+v.eName[nDim])
		bVal.append(v.nameMod[nMod])
		bVal.append(v.eName[nDim])
		print("Value/GS method : "+str(ccc[ind][2+nDim])+"/"+ccc[ind][6])
		bVal.append(ccc[ind][2+nDim])
		print("Window size/step : "+str(ccc[ind][0])+"/"+str(ccc[ind][1]))
		bVal.append(ccc[ind][0])
		bVal.append(ccc[ind][1])
		print("Delay/Complexity : "+str(ccc[ind][4])+"/"+str(ccc[ind][5]))
		bVal.append(ccc[ind][4])
		bVal.append(ccc[ind][5])
		bVal.append(ccc[ind][6])
		print("Use of Bias/Scale : "+str(ccc[ind][7])+"/"+str(ccc[ind][8]))
		bVal.append(ccc[ind][7])
		bVal.append(ccc[ind][8])
		if (nDim == 0):
			print ("Bias/Scaling value arousal : "+str(ccc[ind][9])+"/"+str(ccc[ind][11]))
			bVal.append(ccc[ind][9])
			bVal.append(ccc[ind][11])
		else :
			print("Bias/Scaling value valence : "+str(ccc[ind][10])+"/"+str(ccc[ind][12]))
			bVal.append(ccc[ind][10])
			bVal.append(ccc[ind][12])
		#We print it in graphical form
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(tPlt[:,0], tPlt[:,1], tPlt[:,2+nDim])
		#Labels for axes
		ax.set_xlabel("Window Size")
		ax.set_ylabel("Window Step")
		ax.set_zlabel(v.nameMod[nMod]+" : CCC for "+v.eName[nDim])
		#We show the plot
		plt.pause(0.001)
		plt.show(block=False)
		return bVal
#End printBestValues
