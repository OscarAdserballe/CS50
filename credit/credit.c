#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    unsigned long long int input = get_long("Number: ");

    //checking whether valid or not according to algorithm
    unsigned long long int i;
    int binary = 0;
    int is_valid = 0;
    int sum1;
    int sum2;
    int total;
    unsigned long long int new_num;

    for (i=10; i<input*10; i*=10)
    {
        new_num = input % i;
        new_num = new_num / (i/10);
        //printf("%lli", new_num);
        if (binary == 0)
        {
            sum1 = sum1 + new_num;
            binary = 1;
        }
        else
        {
            unsigned long long int new_num2 = new_num * 2;
            if (new_num2>=10)
            {
                int temp = new_num2 % 10;
                int temp2 = (new_num2-temp)/10;
                new_num2 = temp+temp2;
            }
            sum2 = sum2 + new_num2;
            binary = 0;
        }
    }
    string result;
    total = sum1+sum2;
    if (total % 10 == 0)
    {
        result = "VALID";
        is_valid = 1;
        //printf("VALID\n");
    }
    else
    {
        result = "INVALID";
        //printf("INVALID\n");
    }
    //printf("%i\n", total);

    //checking for what type of card
    int length = log10(i)-1;
    //printf("%i\n", length);
    //checking for credit card generally
    string result2 = "";
    if (length>=13 && length <= 16)
    {
        //Visa if start number 4, luckily loaded in new_num
        //printf("%llu\n", new_num);

        if (new_num == 4) {
            result2 = "VISA\n";
        }
        else if (length == 15)
        {
            result2 = "AMEX\n";
        }
        else if (length == 16)
        {
           result2 = "MASTERCARD\n";
        }
        else
        {
            result = "INVALID";
        }

    }
    printf("%s\n", result);
    if (is_valid == 1)
    {
        printf("%s", result2);
    }
}
