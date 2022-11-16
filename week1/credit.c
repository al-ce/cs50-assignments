#include "cs50.h"
#include <stdio.h>

// declare checksum function
int checksumfunct(long cardnumber);
// declare cardtype function
string cardtype(long cardnumber);


int main(void)
{
    long ognumber;
    ognumber = get_long("Number: ");


    int checkvalid = checksumfunct(ognumber);

    if (checkvalid == 0)
    {
        printf("INVALID\n");
    }
    else
    {
        string whichcard = cardtype(ognumber);
        printf("%s", whichcard);
    }
}



// checksum function
int checksumfunct(long cardnumber)
{
    // checksum to be updated
    long checksum = 0;

    // initialize a place counter
    int place = 1;

    // initialize number to be updated as the original cardnumber is truncated
    long number = cardnumber;

    while (true)
    {
        // if (number - i) == 0
        // then i is the digit at the end of the number
        // Decrease i until number - i == 0
        // reinitialize i to 10 at beginning of loop
        int i = 9;
        while ((number - i) % 10 != 0)
        {
            i --;
        }

        // if place % 2 == 0, then the digit at that place needs to be multiplied by 2 for the checksum
        if (place % 2 == 0)
        {
            i *= 2;
        }
        // increase place counter for next loop
        place += 1;

        // add i to checksum (or i's digits if its greater than 10)
        if (i >= 10)
        {
            checksum += (i - 9);
        }
        else
        {
            checksum += i;
        }

        // check to see if all digits have been added to checksum.
        // If true, break
        if ((number - i) == 0)
        {
            break;
        }

        // divide number by 10 to truncate last digit for next loop
        number /= 10;
    }

    // return pass (1) or fail (0) validity test
    if (checksum % 10 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

string cardtype(long cardnumber)
{
    // AMEX check (15 digit cards in this range)
    if ((cardnumber >= 340000000000000 && cardnumber <= 349999999999999) ||
        (cardnumber >= 370000000000000 && cardnumber <= 379999999999999))
    {
        return "AMEX\n";
    }
    // MC check (16 digit cards in this range)
    else if (cardnumber >= 5100000000000000 && cardnumber <= 5599999999999999)
    {
        return "MASTERCARD\n";
    }
    // VISA check (13 or 16 digit cards beginning with 4)
    else if ((cardnumber >= 4000000000000 && cardnumber <= 49999999999999) ||
             (cardnumber >= 4000000000000000 && cardnumber <= 4999999999999999))
    {
        return "VISA\n";
    }
    else
    {
        return "INVALID\n";
    }
}
