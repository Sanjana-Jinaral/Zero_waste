#dictionary -> a collection of key-value pairs, where each key is unique and maps to a value. Dictionaries are mutable, meaning they can be modified after creation.

chai_types ={"Masala":"Spicy","Adrak":"Ginger","Elaichi":"Cardamom"}
print(chai_types) #{'Masala': 'Spicy', 'Adrak': 'Ginger', 'Elaichi': 'Cardamom'}
print(chai_types["Masala"]) #Spicy
print(chai_types.get("Adrak")) #Ginger

chai_types["Tulsi"] = "Basil" #adds a new key-value pair to the dictionary
print(chai_types) #{'Masala': 'Spicy', 'Adrak': 'Ginger', 'Elaichi': 'Cardamom', 'Tulsi': 'Basil'}

chai_types["Masala"] = "Sweet" #modifies the value of the existing key "Masala"
print(chai_types) #{'Masala': 'Sweet', 'Adrak': 'Ginger', 'Elaichi': 'Cardamom', 'Tulsi': 'Basil'}

for chai in chai_types:
    print(chai) #prints the keys of the dictionary
    print(chai, chai_types[chai]) #prints the key and its corresponding value

for key, value in chai_types.items():
    print(key, value) #prints the key and its corresponding value

#item=key-value pair in the dictionary

if "Masala" in chai_types:
    print("Masala chai is available.") #checks if the key "Masala" exists in the dictionary

chai_types["Earl Grey"] = "Citrus" #adds a new key-value pair to the dictionary

chai_types.pop("Adrak") #removes the key "Adrak" and its corresponding value from the dictionary

chai_types.delete("Elaichi") #removes the key "Elaichi" and its corresponding value from the dictionary
#delect from reference
print(chai_types) #{'Masala': 'Sweet', 'Tulsi': 'Basil', 'Earl Grey': 'Citrus'}

tea_shop = {"chai": {"Masala":"Spicy","Adrak":"Ginger","Elaichi":"Cardamom"},
             "tea": ["black tea", "green tea", "oolong tea", "white tea", "herbal tea"],
             "snacks": {"samosa":"savory","pakora":"crispy"}}
print(tea_shop) #{'chai': {'Masala': 'Spicy', 'Adrak': 'Ginger', 'Elaichi': 'Cardamom'}, 'tea': ['black tea', 'green tea', 'oolong tea', 'white tea', 'herbal tea'], 'snacks': {'samosa': 'savory', 'pakora': 'crispy'}}
print(tea_shop["chai"]["Masala"]) #Spicy
print(tea_shop["chai"])
#{'Masala': 'Spicy', 'Adrak': 'Ginger', 'Elaichi': 'Cardamom'}

squared_numb = {x: x**2 for x in range(10)} #creates a dictionary of numbers and their squares from 0 to 9
print(squared_numb) #{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}

squared_numb.clear() #removes all items from the dictionary
print(squared_numb) #{}

keys = ["a", "b", "c"]
default_value = "blank"
new_dict = dict.fromkeys(keys, default_value) #creates a new dictionary with keys from the list and a default value
print(new_dict) #{'a': 'blank', 'b': 'blank', 'c': 'blank'}

new_dict = dict.fromkeys(keys, keys) #creates a new dictionary with keys from the list and default value of None
print(new_dict) #{'a': ['a', 'b', 'c'], 'b': ['a', 'b', 'c'], 'c': ['a', 'b', 'c']}