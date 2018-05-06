from Pred import Pred
import sys
sys.path.append("../Utils/")
from Setup import setup
sys.path.append("../Config/")
import GlobalsVars as v

def main():
	setup()
	if (len(sys.argv) > 1) :
		arg = sys.argv[1]
		if (arg >= "0" and arg <= str(int(len(v.desc)))):
			Pred(int(arg))
		elif (arg == "help"):
			print("For unimodal prediction, here the correspondance")
			for i in range(len(v.desc)):
				print i,v.nameMod[i]
		else :
			print("Error on arguments")
	else :
		Pred(None)
main()
