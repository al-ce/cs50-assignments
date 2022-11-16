#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // If command line argument isn't passed, remind user of usage and return 1
    if (argc !=2)
    {
        printf("Usage: recover card.raw\n");
        return 1;
    }

    // Open memory card
    FILE *input = fopen(argv[1], "r");
    // if file can't be read, return error
    if (input == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Declare the BYTE type
    typedef uint8_t BYTE;   // BYTE type to read into buffer
    // Initialize some values
    int block_size = 512;   // size of block in the card
    BYTE buffer[block_size]; // buffer to hold block on each read
    int counter = 0;            // counter for how many files have been opened
    char filename[8];       // filename for writing new files
    FILE *output;           // filepointer for output files

    // Repeat until end of card
    // if size of block being read is not 512, end of card = true
    // At the start of each loop, buffer is updated to subsequent block
    while (fread(buffer, 1, block_size, input) == block_size)
    {

        // If start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 &&
            buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0 ))
        {
            // If first JPEG
            if (counter == 0)
            {
                // Get proper name of new file with sprintf()
                sprintf(filename, "%03i.jpg", counter);
                // write first file
                output = fopen(filename, "w");
                // Keep writing to file
                for (int i = 0; i < block_size; i++)
                {
                    fwrite(&buffer[i], sizeof(BYTE), 1, output);
                }
                // increase counter
                counter++;
            }
            // Else
            else
            {
                // close file that you were writing
                fclose(output);
                // Get proper name of new file with sprintf()
                sprintf(filename, "%03i.jpg", counter);
                // open new file
                output = fopen(filename, "w");
                // Keep writing to file
                for (int i = 0; i < block_size; i++)
                {
                    fwrite(&buffer[i], sizeof(BYTE), 1, output);
                }
                // write block to file
                fwrite(&buffer, sizeof(BYTE), block_size, output);
                // increase counter
                counter++;
            }
        }
        // Else
        else
        {
            // If already found JPEG
            if (counter >= 1)
            {
                // Keep writing to file
                for (int i = 0; i < block_size; i++)
                {
                    fwrite(&buffer[i], sizeof(BYTE), 1, output);
                }
            }

        }



    }   // end of while loop

    // At end of card, close open files
    fclose(input);
    fclose(output);

    return 0;
}

