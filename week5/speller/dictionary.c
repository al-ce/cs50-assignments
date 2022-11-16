// Implements a dictionary's functionality

#include <ctype.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>

// TODO: delete these headers
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// initialize word count global variable
int word_count;

// TODO: Choose number of buckets in hash table
// choosing 26^2 for a 'First Two Letters' hash
const unsigned int N =  676;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{

    // Get index word might be found in
    int index = hash(word);

    // Set cursor to start of index
    node *cursor = table[index];

    // TODO: Loop to traverse over linked list
    while (true)
    {
        // If at the end of linked list, word is not found
        if (cursor == NULL)
        {
            return false;
        }

        // Compare word at cursor with argument of function
        int spellcheck = strcasecmp(cursor->word, word);
        // If word found, return true
        if (spellcheck == 0)
        {
            return true;
        }

        // Else, move cursor to next position
        cursor = cursor->next;
    }

}

// Hashes word to a number
unsigned int hash(const char *word)
{

    // Nest 26 indeces (l2) in each letter of the alphabet (l1)
    int l1 = ((int) toupper(word[0]) - 65) * 26;
    int l2 = (int) toupper(word[1]) - 65;

    // TODO: delete this if the function works, otherwise test this as a backup
    /* n = (((int) toupper(word[0]) - 65) * 26) + ((int) toupper(word[1]) - 65); */

    // If word is only one letter long (e.g. 'a')
    // index that word (that letter) into the first hash of that letter
    int length = strlen(word);
    if (length == 1)
    {
       return l1;
    }
    // Else, return index of l1+l2 (e.g. 'ha')
    return l1 + l2;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary to read, and return false if it can't be opened
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Initialize word var to hold word read from file
    char word[LENGTH + 1];

    // Scanf file word by word until end of file is reached
    bool eof_check = false;
    while (eof_check == false)
    {
        int r = fscanf(file, "%s", word);

        // Allocate memory for new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // Copy read word into element `word` at new node
        strcpy(n->word, word);
        n->next = NULL;

        // Get proper index for new node
        int index = hash(word);

        // If table[i] is empty
        if (table [index] == NULL)
        {
            table [index] = n;
        }
        // Point the node to the first element in its corresponding hash index
        else
        {
            n->next = table[index];
            table[index] = n;
        }

        // Increase word count
        word_count++;

        // If at end of file, end loop
        if (r == EOF)
        {
            eof_check = true;
        }
    }

    // Close file and free it from memory
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count - 1;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = table[i];
        while (true)
        {
            if (cursor == NULL)
            {
                free(tmp);
                free(cursor);
                break;
            }
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
