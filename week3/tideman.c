#include "cs50.h"
#include <string.h>
#include <stdio.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

// added function
bool check_cycle(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);



        //_Test that rank choice for last voter matches candidate order
        //_as they were entered as argv
        /* for (int i = 0; i < candidate_count; i++) */
        /* { */
        /*     printf("Rank %i: %i\n", i, ranks[i]); */
        /* } */

        printf("\n");
    }


    // TEST check relative preferences
    /* bool loop; */
    /* while ((loop = true)) */
    /* { */
    /*     printf("Enter two candidates:\n"); */
    /*     int x = get_int("First: "); */
    /*     int y = get_int("\nSecond: "); */
    /*     printf("\n"); */
    /*     printf("Preferred by: %i\n", preferences[x][y]); */
    /*     int cont = get_int("Continue? 1 yes 2 no: "); */
    /*     if (cont == 2) */
    /*         loop = false; */
    /* } */


    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Check for valid vote
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // For each rank, increase relative preference to lower ranked by 1,
    // except for LAST rank
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // p preferred relative to q not preferred
            int p = ranks[i];
            int q = ranks[j];
            preferences[p][q]++;
        }
    }


    // TEST AREA
    /* for (int i = 0; i < candidate_count; i++) */
    /* { */
    /*     for (int j = i + 1; j < candidate_count; j++) */
    /*     { */
    /*         printf("%i relative to %i:\n", i, j); */
    /*         printf("by %i\n", preferences[i][j]); */
    /*     } */
    /* } */
    /* printf("%i", preferences[1][0]); */
    /* printf("%i", preferences[2][0]); */
    /* printf("%i", preferences[2][1]); */
    /* printf("%i", preferences[2][0]); */

    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO


    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;

            }
        }
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO

    // Make a list of corresponding candidate strength
    int strength[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        int w = pairs[i].winner;
        int l = pairs[i].loser;
        strength[i] = preferences[w][l];
    }

    // Sort candidates by strength
    for (int i = 0; i < pair_count; i++)
    {
        // For each iteration through the list,
        // track the strongest candidate,
        // then swap that candidate into the new "strongest" position
        int strength_check = 0;
        int current_strongest = i;
        pair swap_placeholder;
        for (int j = i; j < pair_count; j++)
        {
            if (strength[j] > strength_check)
            {
                strength_check = strength[j];
                current_strongest = j;
            }
        }
        swap_placeholder = pairs[i];
        pairs[i] = pairs[current_strongest];
        pairs[current_strongest] = swap_placeholder;
    }




    // TEST
    /* for (int i = 0; i < pair_count; i++) */
    /* { */
    /*     printf("Pair strength: %i\n", i); */
    /*     printf("Winner: %s\n", candidates[pairs[i].winner]); */
    /*     printf("Loser: %i\n", pairs[i].loser); */
    /* } */


    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        int w = pairs[i].winner;
        int l = pairs[i].loser;

        bool lock_condition = check_cycle(w, l);
        locked[w][l] = lock_condition;
    }


    return;
}

bool check_cycle(int winner, int loser)
{
    // attempting to follow nicknapol82's explainer
    // `winner` remains constant through each recursion, so there's a way
    // to check if a cycle makes it back to the winner of the pair, but
    // loser changes to `i` to move through the 'graph'

    // (check if 'loser beats winner' is already locked in, thus making a cycle)
    if (locked[loser][winner] == true)
    {
        return false;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        // see if loser "wins in any pair that is locked"
        if (locked[loser][i] == true)
        {
            // if so, check whether loser's loser beats winner
            if (check_cycle(winner, i) == false)
            {
                return false;
            }
        }
    }
    return true;
}

// Print the winner of the election
void print_winner(void)
{

    for (int i = 0; i < candidate_count; i++)
    {
        bool source = true;
        for (int j = 0; j < candidate_count; j++)
        {
            // check each column for a given candidate
            // if no "trues" in that column, no one points to that candidate
            // so, they are the source
            if (locked[j][i] == true)
            {
                source = false;
            }
        }
        if (source == true)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }



}
