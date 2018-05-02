#This file contain all the global variables used in the scripts, they can change on each PC
#SET THESE VAR

#GOLD STANDARDS
#Folder for all Gold Standard
gsFolder = "/media/adrien/OS/TER/GS/"
#Path of "Gold Standard"
gsPath = gsFolder+"Ratings/"
#Folder for gold standards
ags = [gsPath+"arousal/",gsPath+"valence/"]
#Folder for individuals gold standards tab
agsi = [gsFolder+"Individual/arousal/",gsFolder+"/Individual/valence/"]

#Template for the ARFF file
arffTempPath = "/home/adrien/Bureau/TER/GIT/scripts_GES/GoldStandardCreation/templateGS.arff"

#THIS PART DOES NOT CHANGE
#System variables
goodColor = '\033[92m'
errColor = '\033[91m'
endColor = '\x1b[0m'

#Number of emotional dimensions and there name
nDim = 2
eName = ["Arousal","Valence"]

#Number of annotators
nAn = 6
