#Author: Adrien Michaud
import sys
import arff
sys.path.append("../Config/")
import GlobalsVars as v
import os

def setupGS():
	try :
		#GoldStandard
		if (os.path.isdir(v.gsPath) == False):
			os.mkdir(v.gsPath)
		if (os.path.isdir(v.gsFolder) == False):
			os.mkdir(v.gsFolder)
		if (os.path.isdir(v.gsConc) == False):
			os.mkdir(v.gsConc)
		if (os.path.isdir(v.agsCreat) == False):
			os.mkdir(v.agsCreat)
		for i in range(len(v.agsc)):
			if (os.path.isdir(v.agsc[i]) == False):
				os.mkdir(v.agsc[i])
	except :
		print("Path for GS Folders must not be ok")	

def setupDescAndGs(modeTest) :
	try :
		endOrNot = True
		print("Creating all the folders necessary if it isn't done yet...")
		#We create all the folders necessary if they don't exist
		for i in range(len(v.desc)):
			#DescriptorFile
			if (os.path.isdir(v.descConc[i]) == False):
				os.mkdir(v.descConc[i])
			if (os.path.isdir(v.descNorm[i]) == False):
				os.mkdir(v.descNorm[i])
		setupGS()
		#We verify that each files for the prediction are here
		print ("Verifying files...")
		for nDim in range(len(v.desc)):
			files = os.listdir(v.desc[nDim])
			wSize = v.sizeBeg[nDim]
			while (wSize <= v.sizeMax[nDim]) :
				wStep = v.stepBeg[nDim]
				while (wStep <= v.stepMax[nDim]) :
					for s in "train","dev","test":
						for i in range(1,v.nbFPart):
							found = False
							name = s+"_"+str(i)+"_"+str(wSize)+"_"+str(wStep)+".arff"
							for f in files:
								if (f.find(name) != -1):
									found = True
							if (found == False):
								#One file is missing
								print(v.nameMod[nDim]+" : "+name+" file is missing !")
								endOrNot = False
					wStep += v.stepStep[nDim]
				wSize += v.sizeStep[nDim]
		#We verify files for gold standard too
		for fold in range(len(v.ags)):
			files = os.listdir(v.ags[fold])
			for s in "train","dev":
				for i in range(1,v.nbFPart):
					found = False
					name = s+"_"+str(i)+".arff"
					for f in files:
						if (f.find(name) != -1):
							found = True
					if (found == False):
						#One file is missing
						print(name+" file is missing !")
						endOrNot = False
		if (modeTest == True):
			for fold in range(len(v.ags)):
				files = os.listdir(v.ags[fold])
				for i in range(1,v.nbFPart):
					found = False
					name = "test_"+str(i)+".arff"
					for f in files:
						if (f.find(name) != -1):
							found = True
					if (found == False):
						#One file is missing
						print(name+" file is missing !")
						endOrNot = False	
		print("End of verifying files")
		print("")
		return endOrNot
	except : 
		print("Check your configuration file, path for Folder must not be ok")

def setup(modeTest):
	return setupDescAndGs(modeTest)
