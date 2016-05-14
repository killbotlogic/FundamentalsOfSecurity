## Simple while loop ##
print("While loop...")
counter = 0
# Instead of using braces { like this }, Python uses indents instead
while counter < 10:
    # Line below is equivalent to counter = counter + 1
    counter += 1
    print(counter)

print()

## Simple for loop ##
print("For loop...")
# range is used to go from one number to another
# range(stop)
# range(start, stop)
# range(start, stop, stepsize)
####
# range(10) or range(0, 10) will produce 0, 1, 2, ..., 9
# range(5, 10) will produce 5, 6, ..., 9
# range(0, 10, 2) will produce 0, 2, 4, 6, 8

# Let's print all even numbers up to 20
for i in range(0, 20, 2):
    print(i)

input("Press Enter to end (for Windows)")
