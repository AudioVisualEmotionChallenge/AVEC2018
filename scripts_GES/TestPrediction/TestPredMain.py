#Author: Adrien Michaud
from TestPred import predictTest
import sys
sys.path.append("../Utils/")
from Setup import setup

def main():
	endOrNot = setup(True)
	if (endOrNot == True):
		predictTest()
	else :
		print ("Error on setup, please check files")

main()
