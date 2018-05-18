#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
import arff
import os
import numpy as np
import sys
sys.path.append(v.labLinearPath)
import liblinearutil as llu

#Open the differents ARFF needed for the matching
def gsOpen(wSize, modeTest):
	gs = {}
	for e in v.eName:
		gs[e] = {}
		for s in v.part:
			if (modeTest != True and s == "test"):
				break
			gs[e][s] = arff.load(open(v.gsConc+s+"_"+e.lower()+".arff","rb"))
	return gs
#End goldStandardOpen

#Apply the gold standards to the differents parameters and treatments
def gsMatch(method, dl, wSize, gs, trainLen, modeTest):
	#Tab who will countain the matching
	vGoldS = {}
	tFD = trainLen/9
	for s in "dev","train","test":
		if (modeTest != True and s == "test"):
			break
		ar = gs['Arousal'][s]['data']
		va = gs['Valence'][s]['data']
		#In the concatenate file, we have 9 files
		tFS = len(ar)/9
		#We get the data for each 9 files
		for i in range(v.nbFPart):
			#For all the value of a file
			for j in range(tFD):
				#The central method is : we take the mid point of earch window
				if (method == "central"):
					calcul = (((float(wSize)/2.0)+v.tsp*float(j)+dl)/v.ts)+float(tFS*i)
					ind = int(calcul)
					if (ind >= tFS+tFS*i):
						ind = tFS+tFS*i-1
					vals = [ar[ind][2],va[ind][2]]
				#Else we use the mean method : we do the mean of each value in the window 
				else :	
					calcul = ((v.tsp*float(j)+dl)/v.ts)+float(tFS*i)
					ind = int(calcul)
					indA = ind+int((float(wSize)/v.ts))
					if (ind >= tFS+tFS*i):
						ind = tFS+tFS*i-1
					if (indA >= tFS+tFS*i):
						indA = tFS+tFS*i-1
					if (indA != ind):
						moy = [0.0,0.0]
						for k in range(ind, indA):
							moy[0] += ar[k][2]
							moy[1] += va[k][2]
						vals = [moy[0]/(indA-ind),moy[1]/(indA-ind)]
					else:
						vals = [ar[ind][2],va[ind][2]]
				if (vGoldS.get(s+"_ind",None) == None):
					vGoldS[s] = []
				vGoldS[s+"_ind"] = ind
				if (vGoldS.get(s,None) == None):
					vGoldS[s] = []
				vGoldS[s].append(vals)
	return vGoldS
#End goldStandardMatch : return a tab countaining the matching
