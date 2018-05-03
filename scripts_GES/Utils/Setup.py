import sys
sys.path.append("../Config/")
import GlobalsVars as v
import os

def folderCreation() :
	try :
		#DescriptorFile
		if (os.path.isdir(v.audioDesc+"Conc/") == False):
			os.mkdir(v.audioDesc+"Conc/")
		if (os.path.isdir(v.audioDesc+"Norm/") == False):
			os.mkdir(v.audioDesc+"Norm/")
		if (os.path.isdir(v.audioDesc+"Descriptors/") == False):
			os.mkdir(v.audioDesc+"Descriptors/")
		#GoldStandard
		if (os.path.isdir(v.gsFolder+"Conc/") == False):
			os.mkdir(v.gsFolder+"Conc/")
		if (os.path.isdir(v.gsFolder+"Ratings/") == False):
			os.mkdir(v.gsFolder+"Ratings/")
	except : 
		print("Check your configuration file, path for folder must not be ok")	

def setup():
	print("Creating all the folders necessary if it isn't done yet...")
	#We create all the folders necessary if they don't exist
	folderCreation()
