#Author: Adrien Michaud
from GSCreation import gsCreation
import sys
sys.path.append("../Utils/")
from Setup import setupGS

def main():
	setupGS()
	gsCreation()

main()
