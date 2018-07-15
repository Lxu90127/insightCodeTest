# -*- coding: utf-8 -*-

import Objects as OBJ

dataCounterMap = OBJ.Trie()

inputFile = open( "itcont.txt", "r")

outputFile = open("top_cost_drug.txt", "w")

idx = 0
for line in inputFile:
    idx = idx + 1
    if idx == 1:
        continue
    string = str(line)
    
    try:
        inputObject = OBJ.InputObject.createInputObject(string)
    except:
        print("invalid String:" + line)
        continue
    
    dataCounterMap.put(inputObject.drug_name, inputObject)
    
    if idx % 100000 == 0:
        print(idx)
    
    
print(idx)

entryList = dataCounterMap.getEntries()
entryList.sort()

# print the title to the output file

print("drug_name,num_prescriber,total_cost", file =outputFile)

entryList.printToFile(outputFile)

inputFile.close()
outputFile.close()