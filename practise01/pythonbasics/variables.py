#1. Python variables
x = 5
y = "John"
print(type(x))
print(type(y))

#2 Variable name
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#3. Multiple Variables
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)


#4. Output Variables
x = 5
y = "John"
print(x, y)


#5. Global Variables
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)