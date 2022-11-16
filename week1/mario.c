#include <stdio.h>

// Issues: can't handle <CR> or char input (scanf() problems)

// Print a square brick of an input size with #
// 1. Get user input n
// 2. Check that input is an int 1-8 (do-while)
// 3. Set counter (i) to 1
// 4. Print n rows with for loop (while i <= n)
//    n + i row = [<space> * (n - i)] + (# * i) + <space> + (# * i)
//       i++

void printhash(int row);

int main(void)
{
    // Get user input until 1 < n < 8
    int n;
    do
    {
        printf("Height: ");
        scanf("%i", &n);
    }
    while (n < 1 || n > 8);
    // For each row
    for (int i = 0; i < n; i++)
    {
        // For each column
        // print n-i blank spaces
        for(int j = 1; j < n - i; j++)
        {
            // Print LEFT side blank spaces
            printf(" ");
        }
        // print hash row left
        printhash(i);
        // print middle blank space (empty "fall" area)
        printf("  ");
        // print hash row right
        printhash(i);
        // print new row
        printf("\n");
    }
}

void printhash(int row)
{
    // print i amount of # (first half)
    for (int k = 0; k <= row; k++)
    {
        printf("#");
    }
}
