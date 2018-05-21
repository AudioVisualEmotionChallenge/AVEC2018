#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
from PredUtils import arffToNan, removeColArff
import os
import arff
import numpy as np

#NORMALISATION OF FILES

#Normalisation of all the features of an ARFF file by modalities
def normFeaturesFile(wSize, wStep, norm, pb, nMod):
	try :
		valKey = {}
		dFile = v.descConc[nMod]+v.tPart+"_"+str(wSize)+"_"+str(wStep)+".arff"
		if (os.path.isfile(dFile) == True):
			#For AUDeep, no normalisation but we need to copy files in norm folder
			if (v.nameMod[nMod] not in v.noNorm):
				#We load the corresponding train descriptor
				dTrain = arff.load(open(dFile,"rb"))
				#We put to Nan ? or None values
				dTrain = arffToNan(dTrain)
				#We loop on all attribute and get the name of it
				for ind, att in enumerate(dTrain['attributes']):
					tabval = []
					for val in dTrain['data']:
						#If this is a None, we must put it to NaN
						if (val[ind] == None or val[ind] == "?"):
							val[ind] = np.nan
						tabval.append(val[ind])
					#We finished to take all the value, we do the mean and std
					mean = np.nanmean(tabval)
					std = np.nanstd(tabval)
					#We stock the values
					key = str(att[0])
					valKey[key] = [mean,std]
			#Now we apply the normalisation on the partitions
			for s in v.part:
				dFile = v.descConc[nMod]+s+"_"+str(wSize)+"_"+str(wStep)+".arff"
				if (os.path.isfile(dFile) == True):
					d = arff.load(open(dFile,"rb"))
					d = arffToNan(d)
					if (v.nameMod[nMod] not in v.noNorm):
						for ind, att in enumerate(d['attributes']):
							for val in d['data']:
								#We update the data
								key = str(att[0])
								if (val[ind] != np.nan):
									val[ind] = (float(val[ind])-float(valKey[key][0]))/float(valKey[key][1])
					#We write the normalised file
					f = open(v.descNorm[nMod]+s+"_"+str(wSize)+"_"+str(wStep)+".arff", "w")
					f.write(arff.dumps(d))
					norm += 1
				else :
					pb += 1
		else :
			pb += 1
		return pb, norm
	except KeyboardInterrupt:
		for s in v.part:
			if (os.path.isfile(dFile) == True):
				os.remove(v.descNorm[nMod]+s+"_"+str(wSize)+"_"+str(wStep)+".arff")
		raise
#End normFeaturesFile

#Normalisation of features
def normFeatures(wSize, wStep, nMod):
	norm = 0
	alNorm = 0
	pb = 0
	f = {}
	nbF = 0
	for s in v.part:
		f[s] = v.descNorm[nMod]+s+"_"+str(wSize)+"_"+str(wStep)+".arff"
		if (os.path.isfile(f[s]) == True):
			nbF += 1
	if (nbF < 3):
		#If only 0/1/2 files have been created, this may be empty or corrupt file, we redo them
		for s in v.part:
			if (os.path.isfile(f[s]) == True):
				os.remove(f[s])
		[pb, norm] = normFeaturesFile(wSize, wStep, norm, pb, nMod)
	else :
		alNorm += 3
	if (v.debugMode == True):
		print(v.nameMod[nMod]+" : Normalised files/was already/problems : "+v.goodColor+str(norm)+v.endColor+"/"+str(alNorm)+"/"+v.errColor+str(pb)+v.endColor)
#End normFeatures

#CONCATENATION OF FILES

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
	if (v.debugMode == True):
		print(v.goodColor+"Concatenation of Gold Standards in progress..."+v.endColor)
	for st in v.ags:
		files = os.listdir(st)
		fNames = {}												
		for f in files :
			for s in v.part:
				if (modeTest == True and s == "test"):
					break
				if (f.find(s) != -1) :
					if (fNames.get(s,None) == None) :
							fNames[s] = []
					fNames[s].append(f)
		for s in v.part:
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
	if (v.debugMode == True):
		print("Concatenated Gold Standards/was already/problems : "+v.goodColor+str(Conc)+v.endColor+"/"+str(AlConc)+"/"+v.errColor+str(Pb)+v.endColor)
	print("")
#End concGoldStandard

#Concatener the recordings per partition (train / dev / test) and per modality
def concFeats(wSize, wStep, nMod):
	Conc = 0
	AlConc = 0
	Pb = 0
	files = os.listdir(v.desc[nMod])
	descf = {}
	fNames = {}
	for f in files :
		for s in v.part:
			if (f.find(s) != -1 and f.find("_"+str(wSize)+"_"+str(wStep)) != -1) :
				if (fNames.get(s,None) == None) :
					fNames[s] = []
				fNames[s].append(f)
	for s in v.part:
		fName = s+"_"+str(wSize)+"_"+str(wStep)+".arff"
		succ = concArff(v.desc[nMod], fNames[s], v.descConc[nMod], fName)
		if (succ == 2):
			AlConc += 1
		elif (succ == 1):
			Pb += 1
		else :
			Conc += 1
	if (v.debugMode == True):
		print(v.nameMod[nMod]+" : Concatenated files/was already/problems : "+v.goodColor+str(Conc)+v.endColor+"/"+str(AlConc)+"/"+v.errColor+str(Pb)+v.endColor)
#End concFeats
