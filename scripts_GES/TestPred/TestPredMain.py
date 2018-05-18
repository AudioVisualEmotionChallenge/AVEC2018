#Author: Adrien Michaud
from TestPred import predictTest
import sys
sys.path.append("../Utils/")
from Setup import setup
sys.path.append("../Config/")
import GlobalsVars as v

def main():
	endOrNot = setup(True)
	if (endOrNot == True):
		for i in range(len(sys.argv)):
			if (sys.argv[i] == "--debug"):
				v.debugMode = True
		predictTest()
	else :
		print ("Error on setup, please check files")

main()
