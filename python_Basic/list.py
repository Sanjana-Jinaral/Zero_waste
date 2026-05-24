#list -> ordered, mutable, allows duplicate elements

tea_varities = ["black tea", "green tea", "oolong tea", "white tea", "herbal tea"]
print(tea_varities)
print(tea_varities[-1])
print(tea_varities[0:3])
print(tea_varities[2:])
tea_varities[4] = "purple tea" 
#["black tea", "green tea", "oolong tea", "white tea", "purple tea"]

tea_varities[1:2]
#["green tea"]
tea_varities[1:2] = "Lemon tea"
#["black tea", "L", "e", "m", "o", "n", " ", "t", "e", "a", "oolong tea", "white tea", "purple tea"]
tea_varities[1:2] = ["Lemon tea"]
#["black tea", "Lemon tea", "oolong tea", "white tea", "purple tea"]

tea_varities[1:3]= ["red tea", "Ginger tea"] 
#["black tea", "red tea", "Ginger tea", "white tea", "purple tea"]

tea_varities.append("yellow tea") #adds at the end of the list
#["black tea", "red tea", "Ginger tea", "white tea", "purple tea", "yellow tea"]
print(tea_varities)

tea_varities[1:1]
#[]
tea_varities[1:1] = ["test","test"] 
#["black tea", "test", "test", "red tea", "Ginger tea", "white tea", "purple tea", "yellow tea"]
print(tea_varities)

for tea in tea_varities:
    print(tea) 
    print(tea, end="-")

if "red tea" in tea_varities:
    print("Red tea is available.")

tea_varities.pop() #removes the last item in the list
#["black tea", "test", "test", "red tea", "Ginger tea

tea_varities.remove #("test") removes the first occurrence of "test" in the list
#["black tea", "test", "red tea", "Ginger tea", "white

tea_varities.insert(2, "yellow tea") #inserts "yellow tea" at index 2
#["black tea", "test", "yellow tea", "red tea", "Ginger tea", "white tea", "purple tea"]
print(tea_varities)

tea_varities_copy = tea_varities.copy() #creates a copy of the list
tea_varities_copy[0] = "white tea" #modifying the copy does not affect the original list
print(tea_varities_copy)

tea_varities_copy = tea_varities #creates a reference to the original list
print(tea_varities_copy)

squared_nums = [x**2 for x in range(10)]#creates a list of squared numbers from 0 to 9
print(squared_nums) #[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

