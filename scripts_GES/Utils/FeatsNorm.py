import sys
sys.path.append("../Config/")
import GlobalsVars as v
from PredUtils import arffToNan
import os
import arff
import numpy as np

#Normalisation of all the features of an ARFF file by modalities
def normFeaturesFile(wSize, wStep, norm, pb, nMod):
	valKey = {}
	dFile = v.descConc[nMod]+v.fconf[nMod]+"_train_"+str(wSize)+"_"+str(wStep)+".arff"
	if (os.path.isfile(dFile) == True):
		#We load the corresponding train descriptor
		dTrain = arff.load(open(dFile,"rb"))
		#We put to Nan ? or None values
		dTrain = arffToNan(dTrain)
		#We loop on all attribute and get the name of it
		for ind, att in enumerate(dTrain['attributes']):
			#We ignore the attributes that must be ignored
			if (str(att[0]) not in v.removedColArff[nMod]):
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
		for s in ('test','dev','train'):
			dFile = v.descConc[nMod]+v.fconf[nMod]+"_"+s+"_"+str(wSize)+"_"+str(wStep)+".arff"
			if (os.path.isfile(dFile) == True):
				d = arff.load(open(dFile,"rb"))
				d = arffToNan(d)
				for ind, att in enumerate(d['attributes']):
					if (str(att[0]) not in v.removedColArff[nMod]):
						for val in d['data']:
							#We update the data
							key = str(att[0])
							if (val[ind] != np.nan):
								val[ind] = (float(val[ind])-float(valKey[key][0]))/float(valKey[key][1])
				#We write the normalised file
				f = open(v.descNorm[nMod]+v.fconf[nMod]+"_"+s+"_"+str(wSize)+"_"+str(wStep)+"_norm.arff", "w")
				f.write(arff.dumps(d))
				norm += 1
			else :
				pb += 1
	else :
		pb += 1
	return valKey, pb, norm
#End normFeaturesFile

#Normalisation of features
def normFeatures(wSize, wStep, nMod):
	norm = 0
	alNorm = 0
	pb = 0
	valAtt = {}
	fTests = v.descConc[nMod]+v.fconf[nMod]+"_test_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	fTrains = v.descConc[nMod]+v.fconf[nMod]+"_train_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	fDevs = v.descConc[nMod]+v.fconf[nMod]+"_dev_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	if (os.path.isfile(fTests) == False or os.path.isfile(fTrains) == False or os.path.isfile(fDevs) == False):
		[valKey, pb, norm] = normFeaturesFile(wSize, wStep, norm, pb, nMod)
		valAtt.update(valKey)
	else :
		alNorm += 3
	print(v.nameMod[nMod]+" : Normalised files/was already/problems : "+v.goodColor+str(norm)+v.endColor+"/"+str(alNorm)+"/"+v.errColor+str(pb)+v.endColor)
	return valAtt
#End normFeatures
