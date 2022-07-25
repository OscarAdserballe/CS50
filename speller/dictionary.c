// Implements a dictionary's functionality
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

int size_dict = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //printf("here?");
    // TODO
    int hash_val = hash(word);
    for (node *tmp = table[hash_val]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 65;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //opening dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Could not open dictionary");
        return 1;
    }
    char load_word[50];
    while (fscanf(dict, "%s", load_word) != EOF)
    {

        if (!check(load_word))
        {
            node *n = malloc(sizeof(node));
            if (n != NULL)
            {
                int hash_val = hash(load_word);
                //printf("%s\n", load_word);
                strcpy(n->word, load_word);
                node *tmp = table[hash_val];
                //printf("%s\n", load_word);
                table[hash_val] = n;
                //printf("%s\n", load_word);
                n->next = tmp;
                size_dict++;
            }
        }
    }
    return true;
    //return 0;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return size_dict;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    return true;
}
