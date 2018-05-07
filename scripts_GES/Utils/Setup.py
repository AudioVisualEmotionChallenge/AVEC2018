import sys
sys.path.append("../Config/")
import GlobalsVars as v
import os

def folderCreation() :
	try :
		for i in range(len(v.desc)):
			#DescriptorFile
			if (os.path.isdir(v.desc[i]) == False):
				os.mkdir(v.desc[i])
			if (os.path.isdir(v.descConc[i]) == False):
				os.mkdir(v.descConc[i])
			if (os.path.isdir(v.descNorm[i]) == False):
				os.mkdir(v.descNorm[i])
		#GoldStandard
		if (os.path.isdir(v.gsPath) == False):
			os.mkdir(v.gsPath)
		if (os.path.isdir(v.gsFolder) == False):
			os.mkdir(v.gsFolder)
		if (os.path.isdir(v.gsConc) == False):
			os.mkdir(v.gsConc)
		if (os.path.isdir(v.agsCreat) == False):
			os.mkdir(v.agsCreat)
		for i in range(len(v.agsc)):
			if (os.path.isdir(v.agsc[i]) == False):
				os.mkdir(v.agsc[i])	
	except : 
		print("Check your configuration file, path for folder must not be ok")	

def setup():
	print("Creating all the folders necessary if it isn't done yet...")
	#We create all the folders necessary if they don't exist
	folderCreation()
