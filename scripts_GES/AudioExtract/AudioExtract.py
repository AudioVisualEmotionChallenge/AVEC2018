import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
import subprocess
import time
import os

#Extract ARFF files for all the audio necessary
def extractAudio(wSize, wStep): 
	extract = 0
	AlExtract = 0
	pb = 0
	current = os.getcwd()
	procs = []
	files = os.listdir(v.daud)
	os.chdir(current)
	#Write in the configuration file the window size and windows step
	conf = "frameMode = fixed \nframeSize = "+str(wSize)+" \nframeStep = "+str(wStep)+" \nframeCenterSpecial = left"
	file(v.inconf,"w").write(conf)
	#Extract the files
	for f in files :
		fi = f.replace(".wav","")
		name = v.fconf+"_"+fi+"_"+str(wSize)+"_"+str(wStep)
		if (os.path.isfile(v.audioDesc+name+".arff") == False):
			if (os.path.isfile(v.daud+f) == True) :
				output = subprocess.Popen([v.oSmile, "-C", v.aconf, "-I", v.daud+f, "-O", v.audioDesc+name+".arff", "2>> ", "log.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current)
				procs.append(output)
				extract += 1
				time.sleep(1)
				if (len(procs) >= v.nbOSmile):
					#Wait for all the subprocess to end
					for i in range(len(procs)):
						procs[i].wait()
					procs = []
			else:
				pb += 1
		else :
			AlExtract += 1
	print("Audio files extracted/was already/problems : "+v.goodColor+str(extract)+v.endColor+"/"+str(AlExtract)+"/"+v.errColor+str(pb)+v.endColor)
#End extractAudio

#Extract all audio with differents wSize/wStep
def audioExtract():
	wSize = v.sizeBeg
	while (wSize <= v.sizeMax) :
		wStep = v.stepBeg
		while (wStep <= v.stepMax) :
			#Extraction of audio recording
			print("Extraction in progress : "+str(wSize)+"/"+str(wStep)+"...")
			extractAudio(wSize, wStep)
			wStep += v.stepStep
		wSize += v.sizeStep
	print("Finished extracting")
#End audioExtract

setup()
audioExtract()
