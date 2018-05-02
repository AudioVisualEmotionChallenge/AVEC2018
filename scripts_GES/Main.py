import sys
import os
from TestPred import predictTest
from AudioPred import audioPred
from GSCreation import gsCreation
from AudioExtract import audioExtract

def folderCreation() :
	#DescriptorFile
	if (os.path.isfile(audioDesc+"Conc/") == False):
		os.mkdir(audioDesc+"Conc/")
	if (os.path.isfile(audioDesc+"Norm/") == False):
		os.mkdir(audioDesc+"Norm/")
	if (os.path.isfile(audioDesc+"Descriptors/") == False):
		os.mkdir(audioDesc+"Descriptors/")
	#GoldStandard
	if (os.path.isfile(gsFolder+"Conc/") == False):
		os.mkdir(gsFolder+"Conc/")


def main():
	#We create all the folders necessary if they don't exist
	folderCreation()
	arg = sys.argv[1]	
	if (arg == "TestPred" or arg == "PredictionTest"):
		predictTest()
	elif (arg == "AudioPred" or arg == "PredictionAudio"):
		audioPred()
	elif (arg == "GSCreation" or arg == "GoldStandardCreation"):
		gsCreation()
	elif (arg == "AudioExtract" or arg == "AudioExtraction"):
		audioExtract()
	else :
		print("Wrong argument")

main()
