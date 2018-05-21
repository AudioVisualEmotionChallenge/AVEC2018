#Author: Adrien Michaud
#This file contain all the global variables used in the scripts
import sys
import os
import platform
from sklearn import linear_model
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
#GOLD STANDARD CREATION
agsCreat = gsFolder+"gs_created/"
agsc = [agsCreat+"arousal/",agsCreat+"valence/"]
#Folder for individuals gold standards tab
agsi = [gsFolder+"individual/arousal/",gsFolder+"/individual/valence/"]
#Var for gs
gsBase = None

#DESCRIPTORS FILES
#Folder for all descriptors
fconf = ["eGeMAPS","","","",""]
audioFeat = c.basePath+"features/audio/"
videoFeat = c.basePath+"features/video/"
physioFeat = c.basePath+"features/physio/"
desc = [audioFeat+"eGeMAPSfunct/",audioFeat+"AUDeep/",videoFeat+"appearance/",videoFeat+"AU/",physioFeat+"ECG/", physioFeat+"HRHRV/", physioFeat+"EDA/", physioFeat+"SCL/", physioFeat+"SCR/"]
nameMod = ["eGeMAPSfunct","AUDeep","appearance","AU","ECG", "HRHRV","EDA","SCL","SCR"]
catMod = ["Audio","Video","Physio"]
catModApp = [["eGeMAPSfunct","AUDeep"],["appearance","AU"],["ECG", "HRHRV","EDA","SCL","SCR"]]
descConc = []
for i in range(len(desc)):
	descConc.append(desc[i]+"Conc/")
descNorm = []
for i in range(len(desc)):
	descNorm.append(desc[i]+"Norm/")
#This is the name of the column we must remove in each descriptors
removedColArff = ["name","class","frameTime","frametime","timeStamp","TimeStamp","timestamp"]
#Name of the modalities that don't need normalisation
noNorm = ["AUDeep"]

#LIBLINEAR
#Path of library LabLinear
labLinearPath = c.labLinearPath

#TEMPLATE FOR GOLD STANDARD
#Template for the ARFF file
arffTempPath = "../GoldStandardCreation/templateGS.arff"

#COLOR VARIABLES
if (platform.system() == "Linux"):
	goodColor = '\033[92m'
	errColor = '\033[91m'
	endColor = '\x1b[0m'
else :
	goodColor = ''
	errColor = ''
	endColor = ''

#DEBUG MODE
debugMode = False
earlystop = 3

#CCC MODE
cccMode = c.cccMode

#FUNCTION USED FOR LINEAR REGRESSION
#0 = unidimentionnal regression/1 = multidimentionnal regression
lFunc =[[linear_model.LinearRegression,0,"RegLin"],[linear_model.Ridge,0,"Ridge"],[linear_model.Lasso,0,"Lasso"],[linear_model.MultiTaskLasso,1,"Multitask-Lasso"], [linear_model.ElasticNet,1,"ElasticNet"],[linear_model.MultiTaskElasticNet,1,"Multitask-ElasticNet"]]
parFunc = [[0.0],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001],
		[0.01,0.001,0.0001,0.00001,0.00001,0.0000001,0.00000001,0.000000001]]
#EMOTIONS (DIMENSIONS)
nDim = 2
eName = ["Arousal","Valence"]

#Number of annotators
nAn = 6
#Number of file per partition
nbFPart = 9
#Name of all partition
part = ['train','dev','test']
tPart = 'train'
aPart = ['dev','test']

#Number of thread for multimodal prediction
nThreads = c.nThreads

#OPTIMISATION FOR AUDIO
#Methods for the gold standards matching
matchGS = ["moy","central"]
#Sampling period of features
ts=0.04
#Sampling period for prediction
tsp=0.4
#Window Size
sizeBeg = [3.0,0.0,3.0,3.0,2.0,2.0,2.0,2.0,2.0]
sizeStep = [1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0,2.0]
sizeMax = [9.0,0.0,9.0,9.0,16.0,16.0,16.0,16.0,16.0]
#Window Step
stepBeg = [0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40]
stepStep = [0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40]
stepMax = [0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40]
#Delay
delBeg = [0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]
delStep = [0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40,0.40]
delMax = [9.60,9.60,9.60,9.60,9.60,9.60,9.60,9.60,9.60]
#Complexity value used for the SVR
C = [0.00001, 0.00002, 0.00005, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
#Value used for the SVR
sVal = 12
