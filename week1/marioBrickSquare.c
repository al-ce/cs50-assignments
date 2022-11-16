#include <stdio.h>


// Print a square  brick of a given size with #

int main(void)
{
    int n;
    do
    {
        printf("Size: ");
        scanf("%i", &n);
    }
    while (n < 1);

    // For each row
    for (int i = 0; i < n; i++)
    {
        // For each column
        for(int j = 0; j < n; j++)
        {
            // Print a brick
            printf("#");
        }
        // Move to next row
        printf("\n");
    }


}
