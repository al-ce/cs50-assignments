#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdio.h>



int main(int argc, string argv[])
{
    // set to number of letters in the alphabet, but change if you want the key
    // to be a different length
    int n = 26;

    // check if user does not provide key or too many args
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // check if key is not exactly 26 letters
    string key = argv[1];
    int keylength = strlen(key);
    if (keylength != n)
    {
        printf("Key must contain %i characters.\n", n);
        return 1;
    }

    // Check to make sure key is all unique alphabet characters
    for (int i = 0; i < (n - 1); i++)
    {
        if (isalpha(key[i]) == 0)
        {
            printf("Key must contain %i characters.\n", n);
            return 1;
        }
        for (int j = 0; j < i; j++)
        {
            if (key[j] == key[i])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }


    // Get plaintext (pt) from user
    string pltxt = get_string("plaintext: ");
    int ptlength = strlen(pltxt);

    printf("ciphertext: ");
    // Convert plaintext to ciphertext w/ cipher
    for (int i = 0; i < ptlength; i++)
    {
        char ptchar = pltxt[i];
        char lowkey = key[ptchar - 97];
        char uppkey = key[ptchar - 65];

        if (islower(ptchar))
        {
            if (islower(lowkey))
            {
                printf("%c", lowkey);
            }
            else
            {
                printf("%c", lowkey + 32);
            }
        }
        else if (isupper(ptchar))
        {
            if (isupper(uppkey))
            {
                printf("%c", uppkey);
            }
            else
            {
                printf("%c", uppkey - 32);
            }
        }
        else
        {
            printf("%c", ptchar);
        }
    }


    // if everything ran successfully, end program
    printf("\n");
    return 0;
}
