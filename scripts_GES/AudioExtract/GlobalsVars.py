#This file contain all the global variables used in the scripts, they can change on each PC
#SET THESE VAR

#DESCRIPTORS FILES
#Folder for all audio descriptor
audioDesc = "/media/adrien/OS/TER/ARFF_Descriptors/"

#SOFTWARES
#OpenSmile base folder
baseFOS = "/home/adrien/Bureau/TER/softwares/opensmile-2.3.0/"
#Number of threads for OSmile Extract
nbOSmile = 8
#Configuration file used and address of it 
fconf = "eGeMAPSv01a"
aconf = baseFOS+"config/gemaps/"+fconf+".conf"
#Address of configuration file for extraction
inconf = baseFOS+"config/shared/FrameModeFunctionals.conf.inc"
#Address for openSmile Extract
oSmile = baseFOS+"inst/bin/SMILExtract"

#AUDIO FILES
#Folder for recording audio
daud = "/media/adrien/OS/TER/Audio_Recordings/Recordings/"

#OPTIMISATION FOR AUDIO
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


#THIS PART DOES NOT CHANGE
#System variables
goodColor = '\033[92m'
errColor = '\033[91m'
endColor = '\x1b[0m'
