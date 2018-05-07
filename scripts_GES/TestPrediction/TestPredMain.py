#Author: Adrien Michaud
from TestPred import predictTest
import sys
sys.path.append("../Utils/")
from Setup import setup

def main():
	setup()
	predictTest()

main()
