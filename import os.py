import os
import heapq
class BinaryTreeNode:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.freq<other.freq
    def __eq__(self,other):
        return self.freq==other.freq
class HuffmanCoding:
    
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}

        
        
        
    def __make_frequency_dict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char]+=1
        return freq_dict
    def __buildHeap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binary_tree_node=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binary_tree_node)
    def __buildTree(self):
        while(len(self.__heap)>1):
            binary_tree_node_1=heapq.heappop(self.__heap)
            binary_tree_node_2=heapq.heappop(self.__heap)
            freq_sum=binary_tree_node_1.freq+binary_tree_node_2.freq
            newNode=BinaryTreeNode(None,freq_sum)
            newNode.left=binary_tree_node_1
            newNode.right=binary_tree_node_2
            heapq.heappush(self.__heap,newNode)
        return
    def __buildCodesHelper(self,root,curr_bits):
        if root is None:
            return 
        if root.value is not None:
            self.__codes[root.value]=curr_bits
            return
        self.__buildCodesHelper(root.left,curr_bits+"0")
        self.__buildCodesHelper(root.right,curr_bits+"1")
    def __buildCodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildCodesHelper(root,"")
    def __getEncodedText(self,text):
        encoded_text=""
        for char in text:
            encoded_text+=self.__codes[char]
        return encoded_text
    def __getPaddedEncodedText(self,encoded_text):
        padded_amount=8-(len(encoded_text)%8)
        
        for i in range(padded_amount):
            encoded_text+='0'
        padded_info="{0:08b}".format(padded_amount)
        encoded_text=padded_info+encoded_text
        return encoded_text
    def __getBytesArray(self,padded_encoded_text):
        array=[]
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            array.append(int(byte,2))
        return array
        
    def compress(self):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name + ".bin"
        with open(self.path,'r+') as file,open(output_path,'wb')as output:
            #make frequency dictionary using the text
            text=file.read()
            text=text.rstrip()
            freq_dict=self.__make_frequency_dict(text)
            #construct the heap from the frequency_dict
            self.__buildHeap(freq_dict)
        #construct the binary tree from the heap
            self.__buildTree()
            self.__buildCodes()
        #creating the encoded text using the codes
            encoded_text=self.__getEncodedText(text)
        #put this encoded text into the binary file
            padded_encoded_text=self.__getPaddedEncodedText(encoded_text)
            bytes_array=self.__getBytesArray(padded_encoded_text)
        #return the binary file as output
            final_bytes=bytes(bytes_array)
            output.write(final_bytes)
        print('Compressed')
        return output_path
path="C:\Users\sured\Desktop\textsur.txt"
h=HuffmanCoding(path)
output_path=h.compress()
