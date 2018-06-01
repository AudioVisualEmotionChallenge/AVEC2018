#Author: Adrien Michaud
import sys
sys.path.append("../Config/")
import GlobalsVars as v
sys.path.append("../Utils/")
from Setup import setup
import subprocess
import time
import os

#OPENSMILE
#File for configuration
fconf = "eGeMAPSv01a"
#OpenSmile base folder
baseFOS = "/home/adrien/Bureau/TER/softwares/opensmile-2.3.0/"
#Number of threads for OSmile Extract
nbOSmile = 4
#Configuration file used and address of it 
aconf = baseFOS+"config/gemaps/"+fconf+".conf"
#Address of configuration file for extraction
inconf = baseFOS+"config/shared/FrameModeFunctionals.conf.inc"
#Address for openSmile Extract
oSmile = baseFOS+"inst/bin/SMILExtract"
#Address for the audio recording
daud = "/media/adrien/OS/TER/recordings/audio/"

#Extract ARFF files for all the audio necessary
def extractAudio(wSize, wStep): 
	extract = 0
	AlExtract = 0
	pb = 0
	current = os.getcwd()
	procs = []
	files = os.listdir(daud)
	os.chdir(current)
	#Write in the configuration file the window size and windows step
	conf = "frameMode = fixed \nframeSize = "+str(wSize)+" \nframeStep = "+str(wStep)+" \nframeCenterSpecial = left"
	file(inconf,"w").write(conf)
	#Extract the files
	for f in files :
		fi = f.replace(".wav","")
		name = fi+"_"+str(wSize)+"_"+str(wStep)
		if (os.path.isfile(v.desc[0]+name+".arff") == False):
			if (os.path.isfile(daud+f) == True) :
				output = subprocess.Popen([oSmile, "-C", aconf, "-I", daud+f, "-O", v.desc[0]+name+".arff", "2>> ", "log.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current)
				procs.append(output)
				extract += 1
				time.sleep(1)
				if (len(procs) >= nbOSmile):
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
	wSize = v.sizeBeg[0]
	while (wSize <= v.sizeMax[0]) :
		wStep = v.stepBeg[0]
		while (wStep <= v.stepMax[0]) :
			#Extraction of audio recording
			print("Extraction in progress : "+str(wSize)+"/"+str(wStep)+"...")
			extractAudio(wSize, wStep)
			wStep += v.stepStep[0]
		wSize += v.sizeStep[0]
	print("Finished extracting")
#End audioExtract
