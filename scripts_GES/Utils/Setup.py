import sys
sys.path.append("../Config/")
import GlobalsVars as v
import os

def folderCreation() :
	try :
		#DescriptorFile
		if (os.path.isdir(v.audioDesc) == False):
			os.mkdir(v.audioDesc)
		if (os.path.isdir(v.audioDescConc) == False):
			os.mkdir(v.audioDescConc)
		if (os.path.isdir(v.audioDescNorm) == False):
			os.mkdir(v.audioDescNorm)
		#GoldStandard
		if (os.path.isdir(v.gsPath) == False):
			os.mkdir(v.gsPath)
		if (os.path.isdir(v.gsFolder) == False):
			os.mkdir(v.gsFolder)
		if (os.path.isdir(v.gsConc) == False):
			os.mkdir(v.gsConc)
	except : 
		print("Check your configuration file, path for folder must not be ok")	

def setup():
	print("Creating all the folders necessary if it isn't done yet...")
	#We create all the folders necessary if they don't exist
	folderCreation()
