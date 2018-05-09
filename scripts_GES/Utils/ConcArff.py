#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from PredUtils import removeColArff
import os
import arff

#Concatenate ARFF files given in one
def concArff(sourceD, fNames, destinationD, fileName):
	try :
		fNames = sorted(fNames)
		arffs = {}
		b = 0
		#We verify that the file dont already exist
		if (not os.path.isfile(destinationD+fileName)) :
			for i in range(len(fNames)):
				if (os.path.isfile(sourceD+fNames[i])):
					#We search for the corresponding descriptor with the parameters
					if (i == 0):
						arffs = arff.load(open(sourceD+fNames[i],"rb"))
					else :
						d = arff.load(open(sourceD+fNames[i],"rb"))
						arffs['data'] += d['data']
				else:
					b = 1
		else :
			b = 2
		if (b == 0):
			f = open(destinationD+fileName, "w")
			arffs = removeColArff(arffs)
			f.write(arff.dumps(arffs))
		return b
	except KeyboardInterrupt:
		os.remove(destinationD+fileName)
		raise
#End concatenationArff : Return 0 if the file is written, 1 if one of the files was missing, 2 if the file already exists

#Concatenation of golds standards per partition (test/dev/train)
def concGs(modeTest):
	Conc = 0
	AlConc = 0
	Pb = 0
	print(v.goodColor+"Concatenation of Gold Standards in progress..."+v.endColor)
	for st in v.ags:
		files = os.listdir(st)
		fNames = {}												
		for f in files :
			for s in "dev","train","test":
				if (modeTest == True and s == "test"):
					break
				if (f.find(s) != -1) :
					if (fNames.get(s,None) == None) :
							fNames[s] = []
					fNames[s].append(f)
		for s in "dev","train","test":
			if (modeTest == True and s == "test"):
				break
			if (st == v.ags[1]):
				succ = concArff(st, fNames[s], v.gsConc, s+"_valence.arff")
			elif (st == v.ags[0]):
				succ = concArff(st, fNames[s], v.gsConc, s+"_arousal.arff")
			if (succ == 2):
				AlConc += 1
			elif (succ == 1):
				Pb += 1
			else :
				Conc += 1
	print("Concatenated Gold Standards/was already/problems : "+v.goodColor+str(Conc)+v.endColor+"/"+str(AlConc)+"/"+v.errColor+str(Pb)+v.endColor)
#End concGoldStandard

#Concatener the recordings per partition (train / dev / test) and per modality
def concRec(wSize, wStep, nMod):
	Conc = 0
	AlConc = 0
	Pb = 0
	files = os.listdir(v.desc[nMod])
	descf = {}
	fNames = {}
	for f in files :
		for s in "test","dev","train":
			if (f.find(s) != -1 and f.find(str(wSize)+"_"+str(wStep)) != -1) :
				if (fNames.get(s,None) == None) :
					fNames[s] = []
				fNames[s].append(f)
	for s in "test","dev","train":
		fName = s+"_"+str(wSize)+"_"+str(wStep)+".arff"
		succ = concArff(v.desc[nMod], fNames[s], v.descConc[nMod], fName)
		if (succ == 2):
			AlConc += 1
		elif (succ == 1):
			Pb += 1
		else :
			Conc += 1
	print(v.nameMod[nMod]+" : Concatenated files/was already/problems : "+v.goodColor+str(Conc)+v.endColor+"/"+str(AlConc)+"/"+v.errColor+str(Pb)+v.endColor)
#End concRecording
