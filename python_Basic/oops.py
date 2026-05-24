'''# 1.Basic Class and Object Creation
# Problem: Create a Car class with attributes like brand and model.Then create an instance of this class.
class Car:
    brand = None
    model = None

my_car = Car()
print(my_car)

class Car:
    def __init__(self, userbrand, model):
        self.brand = userbrand #self is used to refer to the instance of the class
        self.model = model #if we don't use self, the variables will be local to the __init__ method and won't be accessible outside of it

my_car = Car("Toyota", "Camry")
print(my_car.brand)
print(my_car.model)


my_new_car = Car("Honda", "Civic")
print(my_new_car.brand)
print(my_new_car.model)


# __init__ --> constructor (a special method that is called when an object is created)
# it is called first when an object is created and is used to initialize the attributes of the object.

# self --> it is a reference to the current instance of the class and is used to access the attributes and methods of the class.




# 2.Class Method and Self
# Problem: Add a method to the Car class that displays the full name of the car(brand + model).
class Car:
    def __init__(self, brand, model):
        self.brand = brand 
        self.model = model
    def full_name(self): #self : telephone line and interduce themselves
        print(f"using print {self.brand} {self.model}")
        return f"using return {self.brand} {self.model}"
my_car = Car("Toyota", "Camry")
print(my_car.full_name())



# 3.Inheritance
# Problem: Create an ElectricCar class that inherits from the Car class and has an additional attribute for battery_size.
class Car:
    def __init__(self, brand, model):
        self.brand = brand 
        self.model = model
    def full_name(self):
        return f"{self.brand} {self.model}"
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init(brand, model) #super() is used to call the __init__ method of the parent class (Car) to initialize the brand and model attributes
        super().full_name() #super() is used to call the full_name method of the parent class (Car) to display the full name of the car
        self.battery_size = battery_size
my_electric_car = ElectricCar("Tesla", "Model S", "85kwh")
print(my_electric_car.full_name())


# 4.Encapsulation
# Problem: Modify the Car class to encapsulate the brand attribute, making it private, and provide a getter method for it.
class Car:
    def __init__(self, brand, model):
        self.__brand = brand 
        self.model = model
    def get_brand(self):
        return self.__brand
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init(brand, model) #super() is used to call the __init__ method of the parent class (Car) to initialize the brand and model attributes
        super().full_name() #super() is used to call the full_name method of the parent class (Car) to display the full name of the car
        self.battery_size = battery_size
my_electric_car = ElectricCar("Tesla", "Model S", "85kwh")
print(my_electric_car.get_brand())


# Polymorphism
# Problem: Demonstrate polymorphism by defining a method fuel_type in both Car and ElectricCar classes,but with different behaviors.
class Car:
    def __init__(self, brand, model):
        self.__brand = brand 
        self.model = model

    def full_name(self):
        return self.__brand
    
    def fuel_type(self):
        return "Petrol"
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init__(brand, model) #super() is used to call the __init__ method of the parent class (Car) to initialize the brand and model attributes
        super().full_name() #super() is used to call the full_name method of the parent class (Car) to display the full name of the car
        self.battery_size = battery_size
    
    def fuel_type(self):
        return "Electricity"

my_car = Car("Toyota", "Camry")
my_electric_car = ElectricCar("Tesla", "Model S", "85kwh")
print(my_car.fuel_type()) # Output: Petrol
print(my_electric_car.fuel_type()) # Output: Electricity
'''


# Class Variables
# Problem: Add a class variable to Car that keeps track of the number of cars created.
class Car:
    car_count = 0 #class variable to keep track of the number of cars created
    @classmethod
    def __init__(cls, brand, model):
        cls.brand = brand 
        cls.model = model
        Car.car_count += 1 #increment the car_count class variable each time a new car is created

print(Car.car_count) # Output: 0

my_car = Car("Toyota", "Camry")
my_electric_car = Car("Tesla", "Model S")
print(my_car.car_count) # Output: 2
print(Car.car_count) # Output: 2



# Static method(available in the class but not dependent on the instance of the class)
# Problem: add a static method to the Car class that returns a general description of a car.
class Car:
        @staticmethod
        def general_description():
            return "A car is a vehicle that is used for transportation."
        def __init__(self, brand, model):
             self.__brand = brand 
             self.model = model
        def get_brand(self):
             return self.__brand
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init__(brand, model) #super() is used to call the __init__ method of the parent class (Car) to initialize the brand and model attributes
        self.battery_size = battery_size
my_electric_car = ElectricCar("Tesla", "Model S", "85kwh")
print(my_electric_car.get_brand())
print(Car.general_description())


# decoraters --> a function that takes another function as an argument and extends its behavior without explicitly modifying it.
# @login_required(login_url='/login/')

#Property Decorator
# Problem: Use the @property decorator in the Car class to make the model attribute read-only.
class Car:
    def __init__(self, brand, model):
        self.__brand = brand 
        self.__model = model #private not everyone can access it
    @property
    def model(self):
        return self.__model
my_car = Car("Toyota", "Camry")
print(my_car.model) # Output: Camry