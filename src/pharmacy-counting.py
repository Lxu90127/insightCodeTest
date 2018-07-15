# -*- coding: utf-8 -*-

import Objects as OBJ

dataCounterMap = OBJ.Trie()

inputFile = open( "test.txt", "r")

outputFile = open("top_cost_drug.txt", "w")

idx = 0
for line in inputFile:
    idx = idx + 1
    if idx == 1:
        continue
    string = str(line)
    inputObject = OBJ.InputObject.createInputObject(string)
    dataCounterMap.put(inputObject.drug_name, inputObject)

entryList = dataCounterMap.getEntries()
entryList.sort()
entryList.printToFile(outputFile)

inputFile.close()
outputFile.close()

    
            

