import pandas as pd, numpy as np

class Hgrid: 

    def __init__(self, *args, **kwargs):
        return 0 

    def open(hgridDir):
        hgridData  = open(hgridDir)
        hgridLines = hgridData.readlines()

        [nElem,nNode] = np.array(hgridLines[1].split(),dtype=np.int32)
        currentLineNumber = 2
    
        # # # # # # # # # # # # # # # # #
         # # # # READ NODE DATA  # # # #  
        # # # # # # # # # # # # # # # # #
        nodeDataArray = np.zeros([nNode,3])
        for inn, nn in enumerate(range(currentLineNumber,currentLineNumber+nNode)):
            tmpData = np.array(hgridLines[nn].split(),dtype=np.float)
            nodeDataArray[inn] = tmpData[1:4]
            # print(nodeDataArray[nn])
            # print(np.array(hgridLines[nn+2].split(),dtype=np.float)[1:])
        currentLineNumber = currentLineNumber + nNode
        HGRID_DIC = {'Node': nodeDataArray}
        
        print("01. NODE DATA")
        print("    - # of nodes = {}".format(nNode))
        print("    - data shape = {}\n".format(np.shape(nodeDataArray)))

        # # # # # # # # # # # # # # # # #
         # # # # READ ELEM DATA  # # # #  
        # # # # # # # # # # # # # # # # #
        elemDataframe = pd.DataFrame(columns=["triQuad","1","2","3","4"])
        elemDataArray = np.zeros([nElem,4])
        for ine, ne in enumerate(range(currentLineNumber,currentLineNumber+nElem)):
            tmpData = np.array(hgridLines[ne].split(),dtype=np.float)
            if tmpData[1] == 3 :
                elemDataArray[ine][0:4] = tmpData[1:5]
            else :
                elemDataArray[ine] = tmpData[1:6]
            # print(nodeDataArray[nn])
            # print(np.array(hgridLines[nn+2].split(),dtype=np.float)[1:])
        currentLineNumber = currentLineNumber + nElem
        HGRID_DIC['Element'] = elemDataArray

        print("02. ELEMENT DATA")
        print("    - # of elems = {}".format(nElem))
        print("    - data shape = {}\n".format(np.shape(elemDataArray)))

    
        # # # # # # # # # # # # # # # # #
         # #  READ OPEN BOUND DATA # # #  
        # # # # # # # # # # # # # # # # #
        nOpenbc = int(hgridLines[currentLineNumber].split()[0])
        currentLineNumber = currentLineNumber + 1
        nOpenbcNode = int(hgridLines[currentLineNumber].split()[0])
        currentLineNumber = currentLineNumber + 1
        HGRID_DIC["# of Open boundaries"]=nOpenbc

        print("03. OPEN BOUNDARY DATA")
        print("    - # of Open boundaries          = {}".format(nOpenbc))
        print("    - # of Nodes at Open boundaries = {}\n".format(nOpenbcNode))

        for nobc in range(nOpenbc):
            nObcNode = int(hgridLines[currentLineNumber].split()[0])
            currentLineNumber = currentLineNumber + 1
            dict_name = "Obc"+str(nobc+1)
            obcDataArray = np.zeros(nObcNode)
            for intobc, ntobc in enumerate(range(currentLineNumber,currentLineNumber+nObcNode)):
                obcDataArray[intobc] = int(hgridLines[ntobc])
            currentLineNumber = currentLineNumber + nObcNode
            HGRID_DIC[dict_name]=obcDataArray
        
        return HGRID_DIC


if __name__=="__main__":
    hgridDir  = 'read_hgrid_sample.gr3'
    hgrid_dict = read_hgrid(hgridDir)
