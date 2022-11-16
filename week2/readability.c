#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <stdio.h>

// Coleman - Liau index
// index = 0.0588 * L - 0.296 * S - 15.8
// where L is the average number of letters per 100 words in the text, and S is the average number of sentences per 100 words in the text.

int main(void)
{
    // get input from user
    string text = get_string("Text: ");

    // initialize counters and text length
    // 'words' var starts at 1 to account for last word, which won't have a space or .?! to up the counter
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int length = strlen(text);

    // check whether character is a letter, a space, or end a sentence
    // and increase corresponding counter
    for (int i = 0; i <= length; i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
        else if ((int)text[i] == 32)
        {
            words += 1;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }

    // Calculates Coleman-Liau index
    float L = ((float)letters / (float)words) * 100;
    float S = ((float)sentences / (float)words) * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Prints grade level, with lower and upper bounds of below 1 and 16+
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {

        printf("Grade %i\n", index);
    }
}
