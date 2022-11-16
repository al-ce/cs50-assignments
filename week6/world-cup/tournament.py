# Simulate a sports tournament

import csv
import sys
import random

# Number of simulations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    filename = sys.argv[1]

    teams = []
    # TODO: Read teams into memory from file
    # open file using `with` keyword to keep file open only in scope
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # skip first line of csv file
        # next(reader)
        for row in reader:
            # initialize a dictionary for the team in the row
            team = {}
            # assign name and rating from each row to corresponding dict key
            team["team"] = row["team"]
            team["rating"] = int(row["rating"])
            # append dictionary of new team to `teams` list
            teams.append(team)

    counts = {}
    for team in teams:
        counts[team["team"]] = 0

    # TODO: Simulate N tournaments and keep track of win counts
    for i in range(N):
        winner = simulate_tournament(teams)
        counts[winner] += 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO

    # while at least two teams are in the tournament
    while len(teams) >= 2:
        # simulate a round between the original teams and all subsequent winners
        teams = simulate_round(teams)
    # return what should now be the only member of the list,
    # specifically, the key "name" of the dictionary of the winning team
    winner = teams[0]["team"]
    return winner


if __name__ == "__main__":
    main()
