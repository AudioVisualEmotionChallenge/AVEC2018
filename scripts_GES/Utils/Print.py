import GlobalsVars as v
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Print the CCC value and parameters
def printValTest(ccc):
	print("The values are :")
	print(v.eName[ccc[0]]+"\n"
		+"Value Dev:"+str(ccc[1])
		+"\nValue Test:"+str(ccc[2])
		+"\nWindow size:"+str(ccc[3])
		+"\nWindow step:"+str(ccc[4])
		+"\nDelay:"+str(ccc[5])
		+"\nComplexity:"+str(ccc[6])
		+"\nMethod of GS matching:"+ccc[7]
		+"\nUse of Bias:"+str(ccc[8])
		+"\nUse of Scale:"+str(ccc[9])
		+"\nBias value:"+str(ccc[10])
		+"\nScaling value:"+str(ccc[11]))
#End printValue	

#Print the best CCC values
def printBestVal(ccc, tPlt):
	#We take the best values
	ccc = np.array(ccc)
	tPlt = np.array(tPlt)
	iMax = np.zeros(v.nDim)
	for nDim in range(v.nDim):
		iMax[nDim] = np.where(ccc[:,nDim+2] == max(ccc[:,nDim+2]))[0][0]
		#We print the results
		ind = int(iMax[nDim])
		print("The best values are :")
		print(v.eName[nDim]+"\n"
				+"Value:"+str(ccc[ind][2+nDim])
				+"\nWindow size:"+str(ccc[ind][0])
				+"\nWindow step:"+str(ccc[ind][1])
				+"\nDelay:"+str(ccc[ind][4])
				+"\nComplexity:"+str(ccc[ind][5])
				+"\nMethod of GS matching:"+ccc[ind][6]
				+"\nUse of Bias:"+str(ccc[ind][7])
				+"\nUse of Scale:"+str(ccc[ind][8])
				+"\nBias value arousal:"+str(ccc[ind][9])
				+"\nBias value valence:"+str(ccc[ind][10])
				+"\nScaling value arousal:"+str(ccc[ind][11])
				+"\nScaling value valence:"+str(ccc[ind][12]))
		#We print it in graphical form
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(tPlt[:,0], tPlt[:,1], tPlt[:,2+nDim])
		#Labels for axes
		ax.set_xlabel("Window Size")
		ax.set_ylabel("Window Step")
		ax.set_zlabel("CCC for "+v.eName[nDim])
		#We show the plot
		plt.show()
#End printBestValues
