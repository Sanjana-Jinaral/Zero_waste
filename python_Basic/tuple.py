#tuple -> a collection of ordered, immutable, and heterogeneous elements enclosed in parentheses ( ).

tea_types = ("Masala", "Adrak", "Elaichi")
print(tea_types) #('Masala', 'Adrak', 'Elaichi')
print(tea_types[0]) #Masala
print(tea_types[1:3]) #('Adrak', 'Elaichi')

#tea_types[0] = "Tulsi" #TypeError: 'tuple' object does not support item assignment

print(tea_types[-1]) #Elaichi

more_tea_types = ("Tulsi", "Lemon", "Ginger")
all_tea_types = tea_types + more_tea_types #concatenation of tuples
print(all_tea_types) #('Masala', 'Adrak', 'Elaichi',
# 'Tulsi', 'Lemon', 'Ginger')

if "Green" in all_tea_types:
    print("Green tea is available.")

more_tea = ("Herbal", "Earl Grey", "Chamomile","Herbal")
print(more_tea.count("Herbal")) #2
print(more_tea.count("Herbal tea")) #0
print(more_tea.index("Earl Grey")) #1

(black, green, oolong, white, herbal) = tea_types #unpacking a tuple into variables
print(black) #Masala

print(type(tea_types)) #<class 'tuple'>
print(len(tea_types)) #3