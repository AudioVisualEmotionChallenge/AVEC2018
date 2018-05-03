import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
from GSMatching import gsMatch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import signal

#Test function to print the granularity of gold standards
def printGoldStandard():
		tfenetre = v.sizeBeg
		while (tfenetre <= v.sizeMax) :
			fstep = v.stepBeg
			while (fstep < float(tfenetre)) :
				dl = 0
				gs = goldStandardMatch(v.matchGS, dl, tfenetre, fstep)
				#We print the granularity
				plt.plot(np.array(gs['train_ind']),np.array(gs['train'])[:,0])
				fstep += v.stepStep
			tfenetre += v.sizeStep
			plt.show()
#printGoldStandard

#Test function to print the gold standards for each delay
def printGoldStandardDel():
		tfenetre = v.sizeBeg
		while (tfenetre <= v.sizeMax) :
			fstep = v.stepBeg
			while (fstep < float(tfenetre)) :
				dl = 0
				while (dl <= fstep):
					gs = goldStandardMatch(v.matchGS, dl, tfenetre, fstep)
					#We print the granularity
					plt.plot(np.array(gs['train_ind']),np.array(gs['train'])[:,0])
					dl += v.delStep
				plt.show()
				fstep += v.stepStep
			tfenetre += v.sizeStep
#End printGoldStandardDel

def tests():
	print("do nothing for now")

tests()
setup()
