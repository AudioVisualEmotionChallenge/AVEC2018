#This file contain all the global variables used in the scripts, they can change on each PC
#The approch of standardisation is Online in this script

#SET THESE VAR

#DESCRIPTORS FILES
#Folder for all audio descriptor
audioDesc = "/media/adrien/OS/TER/ARFF_Descriptors/"

#SOFTWARES
#Path of library LabLinear
labLinearPath = "/home/adrien/Bureau/TER/softwares/liblinear-2.20/python/"

#GOLD STANDARDS
#Folder for all Gold Standard
gsFolder = "/media/adrien/OS/TER/GS/"
#Path of "Gold Standard"
gsPath = gsFolder+"Ratings/"
#Folder for gold standards
ags = [gsPath+"arousal/",gsPath+"valence/"]

#THIS PART DOES NOT CHANGE
fconf = "eGeMAPSv01a"

#System variables
goodColor = '\033[92m'
errColor = '\033[91m'
endColor = '\x1b[0m'

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
#Complexity value used for the SVR
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
#Value used for the SVR
sVal = 12

#Best values used for prediction on Test
#Value/wSize/wStep/Delay/Complexity/MedianFilter/MethodMatching/BiasUse/ScaleUse/BiasValue/ScaleValue
bAudio = [[0.8,9.0,1.6,4.0,0.01,0,"moy",True,False,-0.018114934492835508,1.1394442116937562], #Arousal
	[0.46,7.0,2.4,3.2,0.05,0,"central",True,False,0.023342096046530064,1.1330534273659931]] #Valence
