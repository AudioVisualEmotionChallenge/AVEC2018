import sys
from TestPred import predictTest
from AudioPred import audioPred
from GSCreation import gsCreation
from AudioExtract import audioExtract

def main():
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
