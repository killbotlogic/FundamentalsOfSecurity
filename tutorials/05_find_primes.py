# Let's write a naive prime number generator

# As we'll be using sqrt, we import math
import math

# We could write this:
# str_num = input("Find primes up to: ")
# highest = int(str_num)
# Or more concisely, just this:
highest = int(input("Find primes up to: "))

print("Let's find all the primes up to (but not including) %d" % highest)
for num in range(2, highest):
    # We started off assuming the number is true
    prime = True
    # Then we test the number against all numbers up to sqrt(num)
    # (sqrt(num) as sqrt(num) ** 2 == num)
    # We also start at two as otherwise all numbers are divisible by one
    for j in range(2, int(math.sqrt(num)+1)):
        # This asks what the remainder is after dividing num by j
        # If it's zero, then j is a factor of num and num isn't prime
        if num % j == 0:
            prime = False
        break
    if prime:
        # Let's print these numbers with a comma at the end instead of a new line
        print(num, end=", ")
print("...")

input("Press Enter to end (for Windows)")
