# import array as arr #importing array module and giving it an alias name arr
from array import *  #we can also import all the functions of the array module using this statement

val = array.array('i',[1,2,3,4,5,6]) #first array model_name .array is for we want to make array
# val = array.array('d',[1.1,2.2,3.3,4.4,5.5,6.6]) #we can also make array of float type using 'd' as the first argument
# val = array.array('u',['a','b','c','d','e','f']) #we can also make array of character type using 'u' as the first argument


print(val) #print the array
print(val[0]) #print the first element of the array

for i in val: #for loop to print all the elements of the array
    print(i, end=" ") #end is used to print the elements in the same line

print("\n")

for i in range(0,6):
    print(val[i] , end=" ") #print the elements of the array using index

print("\n")

for i in range(len(val)): #len is used to get the length of the array
    print(val[i] , end=" , ") #print the elements of the array using index        

print(val.typecode) #typecode is used to get the type of the array
print(val.itemsize) #itemsize is used to get the size of each element in the array
print(val.buffer_info()) #buffer_info is used to get the address of the first element and the number of elements in the array
#print(list(val.reverse())) #reversed is used to get the reversed iterator of the array
print(val.tolist()) #tolist is used to convert the array to a list  
print(val.count(3)) #count is used to count the number of occurrences of an element in the array
print(val.index(4)) #index is used to get the index of the first occurrence of  an element in the array


val.reverse() #reverse is used to reverse the elements of the array
print(val) #print the reversed array

val.append(7) #append is used to add an element at the end of the array
print(val) #print the array after appending an element

val.insert(0,0) #insert is used to add an element at a specific index in the array
print(val) #print the array after inserting an element  

val.remove(3) #remove is used to remove the first occurrence of an element from the array
print(val) #print the array after removing an element

# override
val[0] = 10 #we can also change the value of an element in the array using index
print(val) #print the array after changing the value of an element  


# copy of an array
val2 = val.copy() #copy is used to create a copy of the array
print(val2) #print the copied array

copyArray = array.array(val.typecode, val) #we can also create a copy of the array using the array constructor
print(copyArray) #print the copied array using the array constructor

copyArray = array.array(val.typecode,(x*3 for x in val))
print(copyArray) #print the copied array using the array constructor and a generator expression 

val.pop(3) #pop is used to remove an element at a specific index from the array
print(val) #print the array after popping an element    

val.pop() #pop is used to remove the last element from the array
print(val) #print the array after popping the last element

# A=val[start index: end index]
abc = val[2:5]
aa = val[2:-3]
bb = val[::-1] #we can also reverse the array using slicing 
print(abc,aa,bb)

