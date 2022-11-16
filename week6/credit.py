from cs50 import get_int


def checksum(number):
    """Check card number with Luhn's algorithm"""

    # Initialize checksum to be updated.
    checksum = 0
    # Initialize a place counter representing the column of the card number,
    # right to left.
    place = 1

    # Loop over every number in the card to add it to the checksum function.
    while number != 0:

        # Initialize a counter to use for matching the number in the column
        i = 9
        # If (number - i) == 0, then i is the digit at the end of the number.
        # So, when the while loop condition is met, we can use i to represent
        # the number in the column of the credit card we want to utilize for
        # Luhn's.
        # So, we decrease i in a while loop until number - i == 0 to check all
        # potential digits.
        # At the beginning of the loop, reinitialize i to 9.
        while (number - i) % 10 != 0:
            i -= 1

        # If place % 2 == 0, then the column number is even. So, per Luhn's,
        # the number in that column (represented by i) needs to be multiplied
        # by 2.
        if place % 2 == 0:
            i *= 2

        # Increase the place counter for the next loop.
        place += 1

        # Per Luhn's, add the sum of i's digits to the checksum (so, if
        # i is greater than 10, add (i -9, else add i)
        if i >= 10:
            checksum += i - 9
        else:
            checksum += i

        # Check to see if all digits have been added to checksum, and if true,
        # break. Since we're truncating every tens column on each loop, if
        # number - i == 0, then we've read every column of the number.
        if number - i == 0:
            break

        # Divide the number by 10 to truncate the last digit of the next loop.
        number //= 10

    # return True or False for pass/fail validity test
    if checksum % 10 == 0:
        return True
    else:
        return False


def cardtype(number):
    """Check whether card is MC, Visa, or AmEx based on number"""

    # Variable for various card number ranges
    a = 340000000000000
    b = 349999999999999
    c = 370000000000000
    d = 379999999999999
    e = 5100000000000000
    f = 5599999999999999
    g = 4000000000000
    h = 49999999999999
    i = 4000000000000000
    j = 4999999999999999

    # Check number range and return corresponding type
    if number in range(a, b) or number in range(c, d):
        return "AMEX"
    elif number in range(e, f):
        return "MASTERCARD"
    elif number in range(g, h) or number in range(i, j):
        return "VISA"
    else:
        return "INVALID"

def main():
    """Check to see if credit card number is valid and what brand it is"""
    # Get card number from user.
    number = get_int("Number: ")
    # Check whether card number is valid using Luhn's algorithm.
    if checksum(number) == False:
        print("INVALID")
        quit()
    else:
        print(cardtype(number))
        return 0


main()
