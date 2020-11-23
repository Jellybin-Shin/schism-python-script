import pandas as pd, numpy as np, glob, sys
import shutil

class schipre:
    def __self__(self):
        
        print("")
        
    def save_gr3(self, ipath, opath):
        
        f = open(ipath, 'r'); f_o = open(opath, 'w');

        list_of_lines   = f.readlines()
                        
        i = 1
        numEN           = list_of_lines[i].split();
                
        self.numElements = int(numEN[0]); 
        self.numNodes = int(numEN[1]); i += 1
        
        numOpen = int(list_of_lines[self.numElements+self.numNodes+i].split()[0]); i += 1

        numOpenNodes = int(list_of_lines[self.numElements+self.numNodes+i].split()[0]); i += 1
              
        numLand = int(list_of_lines[self.numElements+self.numNodes+i
                                   +numOpen+numOpenNodes].split()[0]); i += 1
        
        numLandNodes = int(list_of_lines[self.numElements+self.numNodes+i
        
                                   +numOpen+numOpenNodes].split()[0]); i += 1
        
        numLandNodesEach = []
        for nL in range(numLand):
            reviseline = self.numElements+self.numNodes+i+numOpen+numOpenNodes
            numLandNodesEach = list_of_lines[reviseline].split()
            if numLandNodesEach[1] == '10':
                numLandNodesEach[1] = '0'
            elif numLandNodesEach[1] == '11':        
                numLandNodesEach[1] = '1'
            list_of_lines[reviseline] = ' '.join(str(x) for x in numLandNodesEach) +'\n'
            i = i + int(numLandNodesEach[0]) + 1
        
        f_o.writelines(list_of_lines)
        
        f.close()
        f_o.close()


if __name__ == '__main__':
	inputfile = sys.argv[1]
	outputfile = inputfile

	inputpath = "./INPUT/" + inputfile
	outputpath = "./OUTPUT/" + outputfile

	a = schipre()

	a.save_gr3(inputpath, outputpath)
