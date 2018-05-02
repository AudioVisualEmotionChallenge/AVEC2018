#This file contain all the global variables used in the scripts, they can change on each PC
#The approch of standardisation is Online in this script

#fconf = "MFCC1_12_logEnergy_LLD"
#aconf = "./opensmile-2.3.0/config/MFCC/"+fconf+".conf"

#SOFTWARES
#Configuration file used and address of it 
fconf = "eGeMAPSv01a"
aconf = "/home/adrien/Bureau/TER/softwares/opensmile-2.3.0/config/gemaps/"+fconf+".conf"
#Address of configuration file for extraction
inconf = "/home/adrien/Bureau/TER/softwares/opensmile-2.3.0/config/shared/FrameModeFunctionals.conf.inc"
#Address for openSmile Extract
oSmile = "/home/adrien/Bureau/TER/softwares/opensmile-2.3.0/inst/bin/SMILExtract"
#Path of library LabLinear
labLinearPath = "/home/adrien/Bureau/TER/softwares/liblinear-2.20/python/"

#DESCRIPTORS FILES
#Folder for concatenated audio descriptor
aarffdc = "/media/adrien/OS/TER/ARFF_Descriptors/Conc/"
#Folder for normalised audio descriptor
aarffdn = "/media/adrien/OS/TER/ARFF_Descriptor/Norm/"
#Folder for audio descriptor
aarffd = "/media/adrien/OS/TER/ARFF_Descriptors/Descriptors/"

#GOLD STANDARDS
#Path of "Gold Standard"
gsPath = "/media/adrien/OS/TER/GS/Ratings/"
#Folder for gold standards
ags = [gsPath+"arousal/",gsPath+"valence/"]
#Folder for individuals gold standards tab
agsi = ["/media/adrien/OS/TER/GS/Individual/arousal/","/media/adrien/OS/TER/GS/Individual/valence/"]
#Folder for concatenated gold standards
agsn = "/media/adrien/OS/TER/GS/Conc/"

#AUDIO FILES
#Folder for normalised recording audio
daud = "/media/adrien/OS/TER/Audio_Recordings/Recordings/"

#THIS PART DOES NOT CHANGE
#System variables
goodColor = '\033[92m'
errColor = '\033[91m'
endColor = '\x1b[0m'

#Template for the ARFF file
arffTempPath = "/home/adrien/Bureau/TER/templates/templateGS.arff"

#Number of emotional dimensions and there name
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
bAudio = [[0.8,9.0,1.6,4.0,0.01,0,"moy",True,False,-0.018114934492835508,1.1394442116937562], #Arousal
	[0.46,7.0,2.4,3.2,0.05,0,"central",True,False,0.023342096046530064,1.1330534273659931]] #Valence
