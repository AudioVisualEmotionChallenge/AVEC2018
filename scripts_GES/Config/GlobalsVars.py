#This file contain all the global variables used in the scripts
import sys
sys.path.append("../Utils/")
import Config as c

#GOLD STANDARD
#Baseline Folder of Gold Standard
gsFolder = c.basePath+"labels/"
#Path of "Gold Standard"
gsPath = gsFolder+c.gsUse+"/"
gsConc = gsFolder+c.gsUse+"/Conc/"
#Folder for gold standards
ags = [gsPath+"arousal/",gsPath+"valence/"]
#Folder for individuals gold standards tab
agsi = [gsFolder+"individual/arousal/",gsFolder+"/individual/valence/"]

#DESCRIPTORS FILES
#Folder for all audio descriptor eGeMAPS
audioDesc = c.basePath+"features/audio/eGeMAPSfunct/"
audioDescConc = audioDesc+"Conc/"
audioDescNorm = audioDesc+"Norm/"

#OPENSMILE
#OpenSmile base folder
baseFOS = c.baseFOS
#Number of threads for OSmile Extract
nbOSmile = 8
#Configuration file used and address of it 
fconf = "eGeMAPSv01a"
aconf = baseFOS+"config/gemaps/"+fconf+".conf"
#Address of configuration file for extraction
inconf = baseFOS+"config/shared/FrameModeFunctionals.conf.inc"
#Address for openSmile Extract
oSmile = baseFOS+"inst/bin/SMILExtract"

#LIBLINEAR
#Path of library LabLinear
labLinearPath = c.labLinearPath

#AUDIO FILES
#Folder for recording audio
daud = c.basePath+"recordings/audio/"

#TEMPLATE FOR GOLD STANDARD
#Template for the ARFF file
arffTempPath = "../GoldStandardCreation/templateGS.arff"

#COLOR VARIABLES
goodColor = '\033[92m'
errColor = '\033[91m'
endColor = '\x1b[0m'

#EMOTIONS (DIMENSIONS)
nDim = 2
eName = ["Arousal","Valence"]

#Number of annotators
nAn = 6

#OPTIMISATION FOR AUDIO
#Methods for the gold standards matching
matchGS = ["moy","central"]
#Sampling period of features
ts=0.04
#Window Size
sizeBeg = 3.0
sizeStep = 1.0
sizeMax = 9.0
#Window Step
stepBeg = 0.40
stepStep = 0.40
stepMax = 2.80
#Delay
delBeg = 0.00
delStep = 0.40
delMax = 9.60
#Complexity value used for the SVR
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
#Value used for the SVR
sVal = 12

#Best values used for prediction on Test
#Value/wSize/wStep/Delay/Complexity/MedianFilter/MethodMatching/BiasUse/ScaleUse/BiasValue/ScaleValue
bAudio = [[0.8,9.0,1.6,4.0,0.01,"moy",True,True,-0.018114934492835508,1.1394442116937562], #Arousal
	[0.46,7.0,2.4,3.2,0.05,"moy",True,True,0.023342096046530064,1.1330534273659931]] #Valence

