import sys
import unittest


huffmanCipher = {}


def main(argv=None):
    if argv is None:
        argv = sys.argv

    compress("./data.txt")
    decompress("./compressedData.acmp")

    unittest.main()

# Decompress given file
def decompress(fileToDecompress):

    # Open file in binary
    compressedFile = open(fileToDecompress, 'rb')
    byteText = compressedFile.read()
    compressedFile.close()

    # Switch from binary to string
    dataString = byteText.decode()

    # Separate and create huffman cipher dictionary
    byteList = dataString.split("DICT", 1)
    cipher = eval(byteList[1])

    # Reverse the huffman cipher dictionary so that the binary values are now the keys and ascii
    # characters are the values
    reversedCipher = reverseDict(cipher)

    # Parse through bytes and create list of base 2 numbers from the base 10
    binaryList = []
    for byte in byteList[0]:
        x = singleTextToAscii(byte)
        binaryList.append(bin(x))

    # Lookup each base 2 number in the reversed cipher dictionary and save the corresponding character
    decipheredList = []
    for binary in binaryList:
        tempText = binary.split("b")
        decipheredList.append(reversedCipher[tempText[1]])

    # Concatenate strings together and save this final string to the decompressed file
    finalString = ''
    for string in decipheredList:
        finalString = finalString + string

    finishedFile = open("decompressedData.txt", 'w')
    finishedFile.write(finalString)
    finishedFile.close()

# To compress the given file, saves in given savePath
def compress(fileToCompress):


    # Opens file in binary
    numFile = open(fileToCompress, 'rb')
    byteText = numFile.read()
    numFile.close()

    # Create a dictionary of characters and their frequencies
    byteDict = countFreq(byteText)

    # Sorts the dictionary keys by lowest value to highest
    sortedKeys = sortDict(byteDict)

    # Creates initial list of leaf nodes
    listOfNodes = leafNodes(sortedKeys, byteDict)

    # Initializing priority queue with leaf nodes
    pq = priorityQueue()
    for nodes in listOfNodes:
        pq.put(nodes, nodes.value)

    # Given initial priority queue, create huffman tree
    createTree(pq)

    # Given huffman tree, create a huffman cipher
    root = pq.get()
    printTree(root, '')

    # Write out to compressed file
    cipheredList = []
    file2write = open("compressedData.acmp", 'wb')

    # List out numbers according to huffman cipher
    for byte in byteText:
        x = singleAsciiToText(byte)
        cipheredList.append(huffmanCipher[x])

    finalList = []

    # Convert ciphered base 2 numbers to base 10
    for binary in cipheredList:
        finalList.append(int(binary, 2))

    file2write.write(bytes(finalList))
    file2write.write(bytes(('DICT' + str(huffmanCipher)).encode()))

    file2write.close()



# Given byte object of ASCII numbers, creates a dictionary of ASCII keys and the frequency
# of that character as the value
def countFreq(byteText):
    tmpDict = {}
    for bytes in byteText:
        try:
            x = tmpDict[singleAsciiToText(bytes)]
            x = x + 1
            tmpDict[singleAsciiToText(bytes)] = x

        except:
            tmpDict[singleAsciiToText(bytes)] = 1
    return tmpDict

# Create initial leaf nodes
def leafNodes(sortedKeys, byteDict):
    tempNodes = []
    for key in sortedKeys:
        tempNodes.append(node(None, None, byteDict[key], key))
    return tempNodes

# Iterates through tree and creates a huffman cipher based on the node depth
def printTree(nd, turns):

    # print("nd[0].value is ", nd[0].value)
    # print("nd[0].label is ", nd[0].label)

    child1 = nd[0].leftChild
    child2 = nd[0].rightChild

    if child1 == None and child2 == None:
        huffmanCipher[nd[0].label] = turns
        return

    if child1 != None:
        printTree(child1, turns + '0')

    if child2 != None:
        printTree(child2, turns + '1')

# Creates a huffman tree based on the frequencies of the characters
def createTree(pq):
    # pq.printAll()

    if pq.sizeLeft() == 1:
        # pq.printAll()
        return pq

    if pq.sizeLeft() > 1:
        child1 = pq.get()
        child2 = pq.get()

        newLabel = child1[0].label + child2[0].label
        newValue = child1[0].value + child2[0].value

        newNode = node(child1, child2, newValue, newLabel)
        pq.put(newNode, newNode.value)
        createTree(pq)

# Priority Queue data structure
class priorityQueue():

    def __init__(self):
        self.items = {}

    # Returns boolean, tests if queue is empty
    def isEmpty(self):
        return len(self.items) == 0

    # Adds entry as a key into dictionary with the priority being the corresponding value
    def put(self, item, priority):
        self.items[item] = priority

    # Returns the entry with lowest priority
    def get(self):
        keys = self.sortDict()
        toRet = [keys[0], self.items.pop(keys[0])]
        return toRet

    # Prints entire priority queue sorted from lowest to greatest priority
    def printAll(self):
        keys = self.sortDict()

        toPrint = []

        for key in keys:
            toPrint.append([key, self.items[key]])

        print("Priority queue contains ", toPrint)

    # Sorts dictionary,
    def sortDict(self):
        sortedValues = sorted(self.items.values())

        sortedKeys = []
        for values in sortedValues:
            for entry in self.items:
                if self.items[entry] == values:
                    sortedKeys.append(entry)
        return sortedKeys

    # Prints the size of the queue
    def sizeLeft(self):
        return len(self.items)

    # Resets the queue
    def clearQueue(self):
        self.items.clear()

# Node object for the huffman tree
class node(object):
    leftChild = ''
    rightChild = ''
    value = ''
    label = ''

    def __init__(self, leftChild, rightChild, value, label):
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.value = value
        self.label = label

# Sorts given dictionary from smallest value to largest. Returns list of keys from smallest to greatest value
def sortDict(givenDict):
    sortedValues = sorted(givenDict.values())
    sortedKeys = []

    for values in sortedValues:

        for entry in givenDict:
            if givenDict[entry] == values:
                sortedKeys.append(entry)

    return sortedKeys

# Reverse a dictionary, swapping keys with values
def reverseDict(dictionary):
    reversedDict = {}

    for keys in dictionary:
        reversedDict[dictionary[keys]] = keys

    return reversedDict

# Converts single ascii number to it's corresponding ascii character
def singleAsciiToText(number):
    return chr(number)

# Converts single text to ascii number
def singleTextToAscii(text):
    return ord(text)




class Testing(unittest.TestCase):

    # Unit test for the countFreq function. Given byte string and compare to expected dictionary
    def test_countFreq(self):
        self.assertEqual(countFreq(('aabbbcccc').encode()), {'a': 2, 'c': 4, 'b': 3})
        self.assertEqual(countFreq(('abbccc').encode()), {'a': 1, 'c': 3, 'b': 2})
        self.assertEqual(countFreq(('abbcccdddd').encode()), {'d': 4, 'c': 3, 'b': 2, 'a': 1})

    # Unit test for the leafNodes function. Given example dictionary and example list of keys sorted
    # by lowest to greatest values. Compares node values and labels to dictionary keys/values.
    def test_leafNodes(self):
        exampleDict = {'d': 4, 'b': 2, 'c': 3,  'a': 1}
        exampleSortedKeys = ['a', 'b', 'c', 'd']
        x = leafNodes(exampleSortedKeys, exampleDict)

        for nodes in x:
            self.assertEqual(nodes.value, exampleDict[nodes.label])

    # Unit test for the createTree function. Tests that root node has expected label and value
    #  expected for a huffman tree
    # def test_createTree(self):
    #     exampleDict = {'d': 4, 'b': 2, 'c': 3, 'a': 1}
    #     exampleSortedKeys = ['a', 'b', 'c', 'd']
    #     x = leafNodes(exampleSortedKeys, exampleDict)
    #
    #     priorityQ1 = priorityQueue()
    #     for nodes in x:
    #         priorityQ1.put(nodes, nodes.value)
    #     createTree(priorityQ1)
    #     root = priorityQ1.get()
    #     # print(priorityQ1.isEmpty())
    #
    #     self.assertEqual(root[0].label, 'dcab')
    #     self.assertEqual(root[0].value, 10)

    # Unit test for the priorityQueue class. Goes through each function and compares with expected result.
    # def test_priorityQueue(self):
    #
    #     priorityQ2 = priorityQueue()
    #     priorityQ2.printAll()
    #     priorityQ2.put('a', 1)
    #     self.assertEqual(priorityQ2.isEmpty(), False)
    #     self.assertEqual(priorityQ2.get(), ['a', 1])
    #     priorityQ2.put('a', 1)
    #     priorityQ2.put('b', 2)
    #     priorityQ2.put('c', 3)
    #     self.assertEqual(priorityQ2.sizeLeft(), 3)
    #     priorityQ2.clearQueue()
    #     self.assertEqual(priorityQ2.sizeLeft(), 0)
    #     self.assertEqual(priorityQ2.isEmpty(), True)

    # Unit test for the sortDict function.
    def test_sortDict(self):
        unsortedDict = {'d': 4, 'b': 2, 'c': 3, 'a': 1}
        self.assertEqual(sortDict(unsortedDict), ['a', 'b', 'c', 'd'])

    # Unit test for the reverseDict function.
    def test_reverseDict(self):
        straightDict = {'d': 4, 'b': 2, 'c': 3, 'a': 1}
        self.assertEqual(reverseDict(straightDict), {1: 'a', 2: 'b', 3: 'c', 4: 'd'})

    # Unit test for the singleAsciiToText function.
    def test_singleAsciiToText(self):
        self.assertEqual(singleAsciiToText(44), ',')
        self.assertEqual(singleAsciiToText(32), ' ')
        self.assertEqual(singleAsciiToText(103), 'g')
        self.assertEqual(singleAsciiToText(56), '8')


    # Unit test for the singleTextToAscii function.
    def test_singleTextToAscii(self):
        self.assertEqual(singleTextToAscii(','), 44)
        self.assertEqual(singleTextToAscii(' '), 32)
        self.assertEqual(singleTextToAscii('g'), 103)
        self.assertEqual(singleTextToAscii('8'), 56)



if __name__ == '__main__':
        main()
