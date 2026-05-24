#string -> a sequence of characters enclosed in single quotes (' '), double quotes (" "), or triple quotes (''' ''' or """ """). 
# it is mutable, ordered, and allows duplicate characters.

hello = 'world'
print(hello)
print(hello.lower())
print(hello.upper())

fri='  riya  '
print(fri.strip())

frie="dabbu dummi"
print(frie)
print(frie.replace("dabbu","chatu"))

a = "Hello, World!"
print(a.replace("H", "J"))


frien="nitu, diksha, pooja, sneha"
print(frien.split(", "))

friend="sanketha"
print(friend.find("k"))

friends="mush puchi puchi cat"
print(friends.find("S")) #-1 means not found
print(friends.count("puchi"))

chai_type= "Masala"
quantity= 2
order = "I ordered {} cups of {} chai."
print(order.format(quantity, chai_type))

friend_list=["bhavi","vaishnav","kappi","danu","sakshi","teji","varshi","yashuminu"]
print(friend_list[0]) #bhavi
print(friend_list) #['bhavi', 'vaishnav', 'kappi', 'danu

print(" ".join(friend_list)) #bhavivaishnavkappidanusakshitejivarshuyashuminu
print("-".join(friend_list)) #bhavi-vaishnav-kappi-danu-sakshi-teji-varshi-yashuminu
print(", ".join(friend_list)) #bhavi, vaishnav, kappi, danu, sakshi, teji, varshi, yashuminu

print(len(friend))#8

for f in friend:
    print(f)

chai = "he said, \"Masala chai is the best!\"" #/"\ is used to escape the double quotes inside the string
chai1 = "Masala\nchai"

chai2 = r"Masala\nchai" #r before the string indicates that it is a raw string, which means that backslashes are treated as literal characters and not as escape characters.
#r-raw string
chai4 = "c:\\newfolder\\masala.txt" 
#without r, we need to escape the backslashes by using double backslashes (\\) to represent a single backslash in the string.
chai3 = r"c:\newfolder\masala.txt" 
#without r, the \n would be treated as a newline character, and the path would be interpreted incorrectly.

print(chai1)
print(chai2)
print(chai3)

chaic = "Masala Chai"
print("Masala" in chaic) #True



