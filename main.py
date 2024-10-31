# In this assignment, you are going to write a program that counts how many integers entered by the
# user are divisible by 2, 3, and/or 5. The program will ask the user to enter a series of numbers
# separated by a space. If the user enters anything that is not an integer, it should be ignored and not
# included in the count. Then, using a for loop, determine if each number is divisible by 2, 3, and/or 5.
# Once all the numbers have been tested, display a table the list the amount of numbers divisible by
# 2, divisible by 3, and divisible 5.

print("Factors")
print("=-=-=-=")
print()

number = input("Enter a series of numbers separated by a space: ")
print()
current_number = ""
divisible_by_2 = 0
divisible_by_3 = 0
divisible_by_5 = 0

for char in number:
    if char.isdigit() or (current_number == ""):
        current_number += char
    elif char == " " and current_number:
        num = int(current_number)
        if num % 2 == 0:
            divisible_by_2 += 1
        if num % 3 == 0:
            divisible_by_3 += 1
        if num % 5 == 0:
            divisible_by_5 += 1
        current_number = ""
if current_number:
    num = int(current_number)
    if num % 2 == 0:
        divisible_by_2 += 0
    if num % 3 == 0:
        divisible_by_3 += 1
    if num % 5 == 0:
        divisible_by_5 += 1

print("=" * 20)
print(
    "{0:>3s}|{1:<3s}|{2:<3s}".format(
        "Divisible by 2", "Divisible by 3", "Divisible by 5"
    )
)
print("Divisible by 2:", divisible_by_2)
print("Divisible by 3:", divisible_by_3)
print("Divisible by 5:", divisible_by_5)
