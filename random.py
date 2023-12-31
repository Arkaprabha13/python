import random
random_integer=random.randint(10,100)
print("random integer -> ",random_integer)
random_list=[random.randint(10,100) for i in range(10)]
print("A list of 10 randomly generated intgers -> ", random_list)


# using choice() to generate a random number from a
# given list of numbers.
print("A random number from list is : ", end="")
print(random.choice(random_list))
 
# using randrange() to generate in range from 20
# to 50. The last parameter 3 is step size to skip
# three numbers when selecting.
print("A random number from range is : ", end="")
print(random.randrange(20, 50, 3))



# using random() to generate a random number
# between 0 and 1
print("A random number between 0 and 1 is : ", end="")
print(random.random())
 
# using seed() to seed a random number
random.seed(5)
 
# printing mapped random number
print("The mapped random number with 5 is : ", end="")
print(random.random())
 
# using seed() to seed different random number
random.seed(7)
 
# printing mapped random number
print("The mapped random number with 7 is : ", end="")
print(random.random())
 
# using seed() to seed to 5 again
random.seed(5)
 
# printing mapped random number
print("The mapped random number with 5 is : ", end="")
print(random.random())
 
# using seed() to seed to 7 again
random.seed(7)
 
# printing mapped random number
print("The mapped random number with 7 is : ", end="")
print(random.random())


alphabet_list = []

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    alphabet_list.append(letter)



print("\nOriginal list : ")
print(alphabet_list)

# first shuffle
random.shuffle(alphabet_list)
print("\nAfter the first shuffle : ")
print(alphabet_list)

# second shuffle
random.shuffle(alphabet_list)
print("\nAfter the second shuffle : ")
print(alphabet_list)


# using uniform() to generate random floating number in range
# prints number between 5 and 10
print("\nThe random floating point number between 5 and 10 is : ", end="")
print(random.uniform(5, 10))
