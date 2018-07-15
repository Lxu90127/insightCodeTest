# -*- coding: utf-8 -*-
import Objects as OBJ

inputFile = open( "input/itcont.txt", "r")
outputFile = open("output/top_cost_drug.txt", "w")


dataCounterMap = OBJ.Trie()

idx = 0
for line in inputFile:
    idx = idx + 1
    if idx == 1:
        continue
    string = str(line)
    try:
        inputObject = OBJ.InputObject.createInputObject(string)
    except:
    # debug use
    #    print("invalid String:" + line)
        continue
    
    dataCounterMap.put(inputObject.drug_name, inputObject)
    
    # debug use
    #if idx % 100000 == 0:
    #    print(idx)
    
entryList = dataCounterMap.getEntries()
entryList.sort()

# print the title to the output file

print("drug_name,num_prescriber,total_cost", file =outputFile)

entryList.printToFile(outputFile)

inputFile.close()
outputFile.close()
