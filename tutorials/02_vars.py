name = "John"
msg = "Hey there"
a = 2
b = 8

# Both of the next lines are equivalent
# When you have two strings, there are many ways to join them
text = name + ": " + msg # String concatenation
text = "{}: {}".format(name, msg) # Substitute the placeholders {} with the variables
text = "%s: %s" % (name, msg) # Similar to printf in C or Java
# Use whatever you'd prefer and makes sense to you
print(text)

c = a ** b
# For the printf style substitution, %s is for strings and %d is for integers
print("%d to the power of %d is %d" % (a, b, c))
print("Or more concise: %d to the power of %d is %d" % (a, b, a**b))

print()

# For input, you can use the function "input" that will return a string
print("I'm sorry -- I've done all this work and I haven't even introduced myself...")
print("My name's WAL-E -- what's your name?")
name = input()
print("Hi %s, nice to meet you" % name)

input("Press Enter to end (for Windows)")
