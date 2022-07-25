// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    //first 44 bits are the header, copying those

    //array of 44 unsigned 1 byte-size integers
    uint8_t header[HEADER_SIZE];

    //reading input in chunks of 1 for a size of 44 into header array
    fread(header, HEADER_SIZE, 1, input);

    //writing header into output. Size of 44, chunks of 1 byte
    fwrite(header, HEADER_SIZE, 1, output);

    // TODO: Read samples from input file and write updated data to output file
    int16_t buffer;
    while (fread(&buffer, 2, 1, input) == 1)
    {
        int16_t new_value = buffer * factor;
        fwrite(&new_value, 2, 1, output);
    }
    // Close files
    fclose(input);
    fclose(output);
}
