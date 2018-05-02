import GlobalsVars as v
import os
import arff
import numpy as np

#Normalisation of all the features of an ARFF file
def normFeaturesFile(wSize, wStep, norm, pb):
	valKey = {}
	dFile = v.aarffdc+v.fconf+"_train_"+str(wSize)+"_"+str(wStep)+".arff"
	if (os.path.isfile(dFile) == True):
		#We load the corresponding train descriptor
		d = arff.load(open(dFile,"rb"))
		#We loop on all attribute and get the name of it
		for ind, att in enumerate(d['attributes']):
			#We ignore the attributes "name" and "class"
			if (str(att[0]) != "name" and str(att[0]) != "class"):
				tabval = []
				for val in d['data']:
					tabval.append(val[ind])
				#We finished to take all the value, we do the mean and std
				mean = np.nanmean(tabval)
				std = np.nanstd(tabval)
				#We stock the values
				key = str(att[0])
				valKey[key] = [mean,std]
		#Now we apply the normalisation on the partitions
		for s in ('test','dev','train'):
			dFile = v.aarffdc+v.fconf+"_"+s+"_"+str(wSize)+"_"+str(wStep)+".arff"
			if (os.path.isfile(dFile) == True):
				d = arff.load(open(dFile,"rb"))
				for ind, att in enumerate(d['attributes']):
					if (str(att[0]) != "name" and str(att[0]) != "class"):
						for val in d['data']:
							#We update the data
							key = str(att[0])
							val[ind] = (float(val[ind])-float(valKey[key][0]))/float(valKey[key][1])
				#We write the normalised file
				f = open(v.aarffdn+v.fconf+"_"+s+"_"+str(wSize)+"_"+str(wStep)+"_norm.arff", "w")
				f.write(arff.dumps(d))
				norm += 1
			else :
				pb += 1
	else :
		pb += 1
	return valKey, pb, norm
#End normFeaturesFile

#Normalisation of features
def normFeatures(wSize, wStep):
	norm = 0
	alNorm = 0
	pb = 0
	valAtt = {}
	fTests = v.aarffdn+v.fconf+"_test_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	fTrains = v.aarffdn+v.fconf+"_train_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	fDevs = v.aarffdn+v.fconf+"_dev_"+str(wSize)+"_"+str(wStep)+"_norm.arff"
	if (os.path.isfile(fTests) == False or os.path.isfile(fTrains) == False or os.path.isfile(fDevs) == False):
		[valKey, pb, norm] = normFeaturesFile(wSize, wStep, norm, pb)
		valAtt.update(valKey)
	else :
		alNorm += 3
	print("Normalised files/was already/problems : "+v.goodColor+str(norm)+v.endColor+"/"+str(alNorm)+"/"+v.errColor+str(pb)+v.endColor)
	return valAtt
#End normFeatures
