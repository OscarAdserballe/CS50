#include "helpers.h"
#include <stdio.h>
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;
            //average. 3.0 to make sure it has the correct decimal values
            //simplified, i.e. rounded aterwards, such that it is correct
            int average = round((blue + green + red) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
            //printf("%i, %i, %i, %i\n", average, blue, green, red);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            //sepia Red sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
            // sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
            //sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue
            image[i][j].rgbtBlue = round(.272 * red + .534 * green + .131 * blue);
            image[i][j].rgbtGreen = round(.349 * red + .686 * green + .168 * blue);
            image[i][j].rgbtRed = round(.393 * red + .769 * green + .189 * blue);
            //printf("%i, %i, %i, %i\n", average, blue, green, red);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        //temp_array
        RGBTRIPLE temp_array[width];
        for (int j = 0; j < width; j++)
        {
            //image pixels should be flipped inside row
            //image[0][0] top left
            //should become
            //image[0][width-1]
            //so for image[0][j] -> image[0][width - j - 1]
            //issue: needs a copy to imitate -> temp_array for each row
            temp_array[j] = image[i][width - j - 1];
        }
        for (int k = 0; k < width; k++)
        {
            image[i][k] = temp_array[k];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //generate cpy image
    RGBTRIPLE cpy_image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            cpy_image[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int total_red = 0;
            int total_blue = 0;
            int total_green = 0;
            float counter = 0.0;
            //computing average red, green and blue
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    //only counts for every pixel counted
                    //that is, if in a corner, it tests the pixels within a box of radius 1
                    //only if the pixel is within the pixel space does it count it
                    if ((i + k) >= 0 && (i + k) < height && (j + l) >= 0 && (j + l) < width)
                    {
                        total_red = total_red + cpy_image[i + k][j + l].rgbtRed;
                        total_blue = total_blue + cpy_image[i + k][j + l].rgbtBlue;
                        total_green = total_green + cpy_image[i + k][j + l].rgbtGreen;
                        counter = counter + 1.0;
                    }
                }
            }
            image[i][j].rgbtRed = round(total_red / counter);
            image[i][j].rgbtBlue = round(total_blue / counter);
            image[i][j].rgbtGreen = round(total_green / counter);
        }
    }
    return;
}
