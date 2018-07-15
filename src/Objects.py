# -*- coding: utf-8 -*-

####################################################################
# The Input Object is data holder object, which holds the necessary
# data read from one line from the input txt file
####################################################################

class InputObject():
    def __init__(self, first_name, last_name, drug_name, drug_cost):
        self.prescriber_first_name = first_name
        self.prescriber_last_name = last_name
        self.drug_name = drug_name
        self.drug_cost = drug_cost
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "InputObject: <drug_name:%s prescriber_name:%s drug_cost: %s >" % (self.drug_name, self.prescriber_name, self.drug_cost)
    
    # static method
    def createInputObject( string ):
        subString = ""
        isInQuotation = False
        columnNum = 0
        for s in string:
            if s == '"':
                if isInQuotation:
                    isInQuotation = False
                else:
                    isInQuotation = True
                continue
            if s == ',' and isInQuotation is False:
                columnNum = columnNum + 1
                if columnNum == 2:
                    prescriber_last_name = subString.upper()
                if columnNum == 3:
                    prescriber_first_name = subString.upper()
                if columnNum == 4:
                    drug_name = subString
                subString = ""
                continue
            if s == ' ':
                continue
                        
            subString = subString + s
        
        drug_cost = float(subString)
        input_object = InputObject(prescriber_first_name, prescriber_last_name, drug_name, drug_cost)
        return input_object
        
        
##############################################################################
# There are two places that I need to use data structure
# 1. HashSet, where two strings have the same HashCode 
# 2. the children list in trie node
# 3. printing the final result, where I need to put the data out from trie
# and printing the result in desending order (merge sort is a natural choice)
# Thus, I choose linked list with both head and tail implementation which 
#satisfy both requirement in an optimal manner
#############################################################################
        
class LinkedListNode():
    def __init__(self, obj = None):
        self.obj = obj
        self.nextNode = None
        
    def __repr__(self):
        return str(self.obj)
    
    def __str__(self):
        return str(self.obj)
        
class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, obj):
        newNode = LinkedListNode(obj)
        if self.head is None: # first element
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.nextNode = newNode
            self.tail = newNode
            
        self.size = self.size + 1
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        node = self.head
        retString = ""
        while node is not None:
            newPart = str(node)
            if len(retString) == 0:
                retString = newPart
            else:
                retString = retString + ", " + newPart
            node = node.nextNode
        return retString
    
    def contains(self,obj):
        node = self.head
        retVal = False
        while node is not None:
            if node.obj == obj:
                retVal = True
            break
            node = node.nextNode
        return retVal
        
    def sort(self):
        self.head = mergeSortList(self.head)
        self.tail = self.head
        while self.tail is not None:
            self.tail = self.tail.nextNode
            
    def printToFile(self, outputFile):
        node = self.head
        while node is not None:
            print("{},{},{}.".format(node.obj.drug_name, str(node.obj.getNumOfPrescriber()), \
            str(node.obj.getTotalCost())), file =outputFile)
            node = node.nextNode
            
            
##############################################################################
# The following is the implementation of HashSet
# Note that unlike java and cpp, arrays is not the basic data structure in python
# rather, list is the basic data structure, thus, I have to use it for quick access
# for hashset implementation
#############################################################################
            
class HashSet():
    def __init__(self):
        self.table = []
        idx = 0
        while idx <= 26*26 + 1: # additonal one spot for none first or last name
            idx = idx + 1
            self.table.append([])
            
    def add( self, firstName, lastName):
        fullName = firstName + ',' + lastName
        if len(firstName) == 0 or len(lastName) == 0:
            nameIdx = 0
        else:
            firstNameInitial = ord(firstName[0]) - ord('A')
            lastNameInitial = ord(lastName[0]) - ord('A')
            nameIdx = lastNameInitial * 26 + firstNameInitial + 1
        
        targetList = self.table[nameIdx]
        isInputNameExists = False
        for name in targetList:
            if name == fullName:
                isInputNameExists = True
                break
        
        if isInputNameExists is False:
            targetList.append(fullName)
            
    def getSize(self):
        totalSize = 0
        idx = 0
        while idx <= 26*26:
            currentlistSize = len(self.table[idx])
            totalSize  = totalSize + currentlistSize
            idx = idx + 1
        return totalSize
            
##############################################################################
# The following Object is trying to implement a replacement of HashMap and HashSet
# namely --- Trie
# I am going to implment TrieNode and Trie
# the insert complexity is O(m) where m stands for the length of the drug_name
# chars. Which is can be considered as O(1)
#############################################################################

class TrieNode():
    def __init__(self, char):
        self.char = char
        # here I use the data structure List, I assume it is OK, as I am not 
        # using any advance functionality. 
        # it is very ez to replace it with a self-coded linked list, array or 
        # a table with 26 chars
        self.children = []
        self.isMainNode = False
        # depend on whether containedObject is None or not, the Trie can be 
        # used as HashTable or HashMap
        self.containedObject = None 
        

class Trie():
    def __init__(self):
        self.root = TrieNode("")
        self.size = 0;
        
    def getSize(self):
        return self.size
        
    def put(self, string: str, inputObject = None):
        node = self.root
        isIncreaseSizeByOne = False
        for char in string:
            foundInChilren = False
            for child in node.children:
                if child.char == char:
                    node = child
                    foundInChilren = True
                    break

            if not foundInChilren:
                isIncreaseSizeByOne = True
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node
        
        # if the node is not on the leaf of the tree - no new branch but not main node
        if isIncreaseSizeByOne is False and node.isMainNode is False: 
            isIncreaseSizeByOne = True
            
        node.isMainNode = True
        if inputObject is not None:
            if node.containedObject is None:
                node.containedObject = ContainedObject(inputObject)
            else:
                node.containedObject.add(inputObject)
            
        if isIncreaseSizeByOne:
            self.size = self.size + 1
        
    def get(self, string: str):
        node = self.root
        isStringExist = True
        for char in string:
            foundInChilren = False
            for child in node.children:
                if child.char == char:
                    node = child
                    foundInChilren = True
                    break
                
            if not foundInChilren:
                isStringExist = False
                break
        
        if isStringExist and node.isMainNode:
            return node
        else:
            return None
              
    def contains(self, string: str):
        node = self.get(string)
        if node is not None:
            return True
        else:
            return False
    
    # perform DFS to get all objects saved in trie
    def getKeys(self):
        retList = LinkedList()
        initialString = ""
        dfsHelper(self.root, retList, initialString, False )
        return retList
        
    def getEntries(self):
        retList = LinkedList()
        initialString = ""
        dfsHelper(self.root, retList, initialString, True)
        return retList
    
    # preString is None, get all Keys
    # preString is not None, get All Entries


##############################################################################
# Contained Object 
# we can use directly use InputObject as ContainedObject, but we should not 
# do that as it requires more memory than required
#############################################################################

class ContainedObject():
    def __init__(self, inputObject : InputObject):
        self.drug_name = ""
        self.total_cost = inputObject.drug_cost
        self.prescriber_name_set = HashSet()
        self.prescriber_name_set.add(inputObject.prescriber_first_name, inputObject.prescriber_last_name )
        
    def add(self, inputObject: InputObject):
        self.total_cost = self.total_cost + inputObject.drug_cost
        self.prescriber_name_set.add(inputObject.prescriber_first_name, inputObject.prescriber_last_name)

    def getTotalCost(self):
        return self.total_cost
    
    def getNumOfPrescriber(self):
        return self.prescriber_name_set.getSize()
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "ContainedObject: <drug_name:%s total_cost:%s prescriber #: %s >" % \
        (self.drug_name, self.getTotalCost(), self.getNumOfPrescriber())
        

      
##############################################################################
# HELPER METHODS
#############################################################################   
        
def dfsHelper(node, resList, preString, isEntry):
    if isEntry is False:
        currentString = preString + node.char
        if node.isMainNode:
            resList.append(currentString)
            
        listNode = node.children.head
        while listNode is not None:
            child = listNode.obj
            newString = str(currentString)
            dfsHelper(child, resList, newString, isEntry)
            listNode = listNode.nextNode
    else:
        currentString = preString + node.char
        if node.isMainNode:
            node.containedObject.drug_name = currentString
            resList.append(node.containedObject)
        
        for child in node.children:
            newString = str(currentString)
            dfsHelper(child, resList, newString, isEntry)
            
def mergeSortList( node : LinkedListNode):
    if node is None or node.nextNode is None:
        return node;
        
    #step 1. cut the list in middle
    prevNode = None
    slowPointer = node
    fastPointer = node
    
    while fastPointer is not None and fastPointer.nextNode is not None:
        prevNode = slowPointer
        slowPointer = slowPointer.nextNode
        fastPointer = fastPointer.nextNode.nextNode

    prevNode.nextNode = None
    
    #step 2. sort first half list and second half list seperately
    sortedNode1 = mergeSortList(node);
    sortedNode2 = mergeSortList(slowPointer);
    
    # step 3. merge two sorted list
    return mergeTwoSortedList(sortedNode1, sortedNode2)
    
def mergeTwoSortedList(node1 : LinkedListNode, node2 : LinkedListNode):
    dummyNode = LinkedListNode()
    currentNode = dummyNode;
    while node1 is not None and node2 is not None:
        if node1.obj.total_cost >= node2.obj.total_cost:
            currentNode.nextNode = node1
            node1 = node1.nextNode
        else:
            currentNode.nextNode = node2
            node2 = node2.nextNode
        currentNode = currentNode.nextNode
    
    if node1 is not None:
        currentNode.nextNode = node1
    
    if node2 is not None:
        currentNode.nextNode = node2
    
    return dummyNode.nextNode
    
    
        
        
        
    
         
        


        
    

        
