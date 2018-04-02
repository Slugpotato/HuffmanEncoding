# HuffmanEncoding
An example of huffman encoding to compress and decompress ASCII art in a lossless way. 

Tutorial link: 
http://designingafuture.com/tutorials/huffmanEncoding

==========================
Disclaimer:
==========================
This does not reduce the size of the orginal file as intended. It successfully encodes the data using huffman encoding, however I could not figure out a way to edit a file on the bit level, therefore the 'compressed' file remains about the same size as the original file. Had I found a way to replace the original bytes with the much smaller bit sequences as the cipher dictates, it would be a much more compressed file. 


==========================
Summary:
==========================

Huffman encoding: 
https://en.wikipedia.org/wiki/Huffman_coding

The code takes in the data from data.txt as binary and creates a huffman tree similar to the one shown here:
![](./huffmanEncoding.jpg?raw=true "Huffman Tree for data in data.txt file")

Using this tree, the code then creates a Huffman cipher, where the left branches are zeros and the right branches are ones. This cipher ends up looking like this: 

{'@': '101', '#': '100110', ',': '0', '+': '1000', ';': '1001000', ' ': '11', ':': '1001001', "'": '100101', '\n': '100111'}

The idea is to replace a byte, say the byte that represents the character '@', with a shorter sequence of bits. In this case it would be the bits '101', and would save the file the five remaining bits everytime this character is in the file. The most frequent characters, like the ',' character, would be replaced with even shorter sequences. Combined together, this encoding significantly reduces the space needed to store the data. Or at least that's the idea, as I could not edit the file on the bit level. Currently it replaces the original data with the ASCII symbol that corresponds with the original binary number intended by the cipher. For example, the cipher replaces the character ',' with the bit sequence '0', so the code currently replaces every ',' character with the 'NUL' character. The encoded data is saved to a file labeled 'compressedData.acmp', which is short for 'Andrew Compression' :D

After storing the encoded data, the code also stores the cipher for use in decoding. Decompressing works by reversing the saved cipher, changing the initial characters back to their binary sequences, and matching the sequences to their corresponding original characters. Finally, this is saved to a decompressedData.txt file.

==========================
To run this code:
==========================

The only two lines that one should have to edit are lines 12 and 13 in the main function, that is the actual calls to the compress and decompress functions.

compress("./data.txt")
decompress("./compressedData.acmp")

You can change the path of the files to compress a different file, though the compressed file is generated through the compression function so I would advise not changing this path. 


==========================
Unit tests
==========================

There are numerous unit tests at the end of the file, utilizing the unittest python library. Should you wish to run either the 'test_createTree()' or 'test_priorityQueue()' unit tests, they must be done separately as there is only one instance of the priority queue allowed at one time. Therefore if you wish to uncomment the 'test_createTree()' function for unit testing for example, leave the 'test_priorityQueue()' function commented and also comment out the 'compress("./data.txt")' call in main.



That's it, I hope you enjoy the project! Please feel free to let me know if you figure out how to edit a file on a bit level because that will definitely bother me! >:(



