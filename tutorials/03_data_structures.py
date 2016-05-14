my_int = 10

my_float = 0.3

my_str = "Meow"

my_list = [1, 3, 5, 7, 9]

# To work out the length of a string or list, you can use len(obj)

# Go from the 0th entry of my_list to the nth entry
for i in range(len(my_list)):
    # Longer: my_list[i] = my_list[i] * 2
    # Or shorter...
    my_list[i] *= 2
print(my_list)

my_list = ["cat", "dog", "mouse", "rat"]
# Append adds horse to the end of my_list
my_list.append("horse")
print(my_list)
# Pop takes the last element off by default
print(my_list.pop())
# Pop can also be told to take a specific element away
print(my_list.pop(0))
# You can iterate over a list quite simply
for animal in my_list:
    print("My animal is a", animal)
# You can also iterate using a range()
# (more details in the loop instructional video)
for i in range(len(my_list)):
    print("The animal in stable %d is a %s" % (i, my_list[i]))

# Dictionaries are hash tables
# They map a key to a value
my_dict = {"dog": "woof", "cat": "meow"}
my_dict["cow"] = "moo"
# Below is the same as calling 'for animal in my_dict.keys():'
for animal in my_dict:
    print("The %s says %s" % (animal, my_dict[animal]))
# We can also make it more descriptive and easier to follow
for animal, sound in my_dict.items():
    print("The %s says %s" % (animal, sound))
