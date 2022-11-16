# NOTE: movies.db schema:

# CREATE TABLE movies (
#                     id INTEGER,
#                     title TEXT NOT NULL,
#                     year NUMERIC,
#                     PRIMARY KEY(id)
#                 );
# CREATE TABLE stars (
#                 movie_id INTEGER NOT NULL,
#                 person_id INTEGER NOT NULL,
#                 FOREIGN KEY(movie_id) REFERENCES movies(id),
#                 FOREIGN KEY(person_id) REFERENCES people(id)
#             );
# CREATE TABLE directors (
#                 movie_id INTEGER NOT NULL,
#                 person_id INTEGER NOT NULL,
#                 FOREIGN KEY(movie_id) REFERENCES movies(id),
#                 FOREIGN KEY(person_id) REFERENCES people(id)
#             );
# CREATE TABLE ratings (
#                 movie_id INTEGER NOT NULL,
#                 rating REAL NOT NULL,
#                 votes INTEGER NOT NULL,
#                 FOREIGN KEY(movie_id) REFERENCES movies(id)
#             );
# CREATE TABLE people (
#                 id INTEGER,
#                 name TEXT NOT NULL,
#                 birth NUMERIC,
#                 PRIMARY KEY(id)
#             );

# WARNING: n.b.: movies.db only contains movies from 1970 onwards

from cs50 import SQL

# Use URI to open the movies.db database in the current folder
db = SQL("sqlite:///movies.db")
# Use db.execute commands to run SQL commands inside Python

# NOTE: Useful functions:

def print_movie_list(movies: list):
    """Print movie titles in a returned list of dicts with
    'title': 'movie title' structure."""
    for movie in movies:
        print(movie['title'])


def get_year():
    """Get desired year to query from user."""

    # Get year from user. Only accept integers.
    while True:
        try:
            year = int(input("Year: "))
            break;
        except ValueError:
            print("Invalid input: only use numbers.\n")
    return year


def get_movie():
    """Get desired movie to query from user."""
    return(input("Title: ").strip())


# NOTE: Fun functions for experimenting:


def movie_dir():
    """Get user input of a movie title and its release year.
    Return that movie's director. Assuming unique title per year."""
    title = get_movie()
    year  = get_year()

    # Get the name from the table `people` whose id matches the person_id
    # from the table `directors` whose movie_id matches the id
    # from the table `movies` whose title and year match the user's input.
    sql = "SELECT name FROM people WHERE id IN " \
        "(SELECT person_id FROM directors WHERE movie_id IN " \
        "(SELECT id FROM movies WHERE title = ? AND year = ?))"

    # Returns a list with a single item: a dictionary with key: value pair 'name': "Director's name"
    director = db.execute(sql, title, year)
    print(f"Director: {director[0]['name']}")

# NOTE: Uncomment to run in main()
# movie_dir()
# ❯ py movies.py
# Title: Titanic
# Year: 1997
# Director: James Cameron


def yearly_avg():
    """Print yearly average rating of movies in order of highest rated year first."""
    sql = "SELECT AVG(ratings.rating) AS average, movies.year " \
        "FROM ratings JOIN movies ON movies.id = ratings.movie_id " \
        "GROUP BY year ORDER BY AVG(ratings.rating) DESC"
    yearly_avg_ratings = db.execute(sql)

    print(f"Average |    Year")
    print("-----------------")
    for rating in yearly_avg_ratings:
        avg = f"{rating['average']:.2f}"
        year = rating['year']
        print(f"{avg:5}   |    {year:<4}")


# NOTE: Uncomment to run in main()
# yearly_avg()



# NOTE: Problem Set 7 'movies.db' related functions

# PERF: 1. Write a SQL query to list the titles of all movies released in 2008
def movies_by_year():
    """Get user input of a year and write all movies released that year to a
    text file."""

    year  = get_year()

    # Get all titles from the table `movies` whose year is equal to user input.
    sql = 'SELECT title FROM movies WHERE year = ?'

    # Store all matching movies in a file
    movies = db.execute(sql, year)
    # Write movies to a .txt file
    filename = f"{year}movies.txt"
    with open(filename, "w") as file:
        # Write a "header"
        file.write(f"IMDb: Movies released in {year}\n\n")
        # iterate through stored list and write all movies to file
        for movie in movies:
            file.write(f"{movie['title']}\n")

    print(f"List of {year} movies written to {filename}")
    print(f"Total number of movies released in {year}: {len(movies)}")

# NOTE: Uncomment to run in main()
# movies_by_year()
# ❯ py movies.py
# Year: 1999
# List of 1999 movies written to 1999movies.txt
# Total number of movies released in 1999: 4863


# PERF: 2. Write a SQL query to determine the birth year of a person from user's input.
def person_birthyear():
    """Get a person from the user. Cross reference the tables in movies.db to
    determine that person's year of birth."""

    # Lowercase both user's input and the db query to allow for user input
    # variance (e.g. GoLDie HAwN, goldie hawn, GOLDIE HAWN, etc. )
    person = input("Person: ").lower()
    sql = 'SELECT birth FROM people WHERE LOWER(name) = ?'

    year = db.execute(sql, person)
    print(f"Born: {year[0]['birth']}")

# NOTE: Uncomment to run in main()
# person_birthyear()
# ❯ py movies.py
# Person: Goldie HAWN
# Born: 1945


# PERF: 3. Write a SQL query to list the titles of all movies with a release date on or after 2018, in alphabetical order.
def released_after_year():
    """Get user input of a year and write all movies released on that year and
    beyond to a text file."""

    year  = get_year()

    # Query by minimum year and sort returned items by year
    sql = 'SELECT title, year FROM movies WHERE year >= ? ORDER BY title'

    # Store all matching movies in a file
    movies = db.execute(sql, year)
    # Write movies to a .txt file
    filename = f"{year}+movies.txt"
    with open(filename, "w") as file:
        # Write a "header"
        file.write(f"IMDb: Movies released in {year} and beyond\n\n")
        # iterate through stored list and write all movies to file
        for movie in movies:
            file.write(f"{movie['title']}, {movie['year']}\n")

    print(f"List of {year}+ movies written to {filename}")
    print(f"Total number of movies released in {year}+: {len(movies)}")

# NOTE:
# released_after_year()
# ❯ py movies.py
# Year: 2018
# List of 2018+ movies written to 2018+movies.txt
# Total number of movies released in 2018+: 69705


# PERF:  4. Write a SQL query to determine the number of movies with an IMDb rating of 10.0.
def perfect_ten():
    """Print the number of movies with a perfect 10.0 score."""

    sql = "SELECT COUNT(title) FROM movies WHERE id IN " \
        "(SELECT movie_id FROM ratings WHERE rating = 10.0)"
    perfect10 = db.execute(sql)

    print_movie_list(perfect10)

# NOTE: Uncomment to run in main()
# perfect_ten()


# PERF: 5. Write a SQL query to list the titles and release years of all Harry Potter movies, in chronological order.
def franchise_chron():
    """Get user input of a string and print all movies with that string in
    the title in chronological order."""

    s = input("Franchise title: ")

    # This condition prevents user from giving too vague a request,
    # or worse, null input.
    if len(s) < 3:
        franchise_chron()
        return

    # Add % wildcards around user's input. The execute() command
    # won't recognize characters around the ? variable input char,
    # so we pass everything we need to it ahead of time.
    s = f"%{s}%"
    sql = 'SELECT title FROM movies WHERE title LIKE(?) ORDER BY year'
    franchise = db.execute(sql, s)
    print_movie_list(franchise)

# NOTE: Uncomment to run in main()
# franchise_chron()
# ❯ py movies.py
# Franchise title: rd of the rings
# The Lord of the Rings
# The Lord of the Rings: The Fellowship of the Ring
# The Lord of the Rings: The Two Towers
# The Lord of the Rings - The Appendices Part 1: From Book to Vision
# The Lord of the Rings: The Return of the King
# ...etc.etc....


# PERF: 6. Write a SQL query to determine the average rating of all movies released in 2012.
def year_avg_rating():
    """Get user input of year and return average rating of all movies that year."""

    year  = get_year()

    sql = "SELECT AVG(rating) AS average FROM ratings " \
        "WHERE movie_id IN (SELECT id FROM movies WHERE year = ?)"

    avg = db.execute(sql, year)
    print(f"{avg[0]['average']:.2f}")



# NOTE: Uncomment to run in main()
# year_avg_rating()
# ❯ py movies.py
# Year: 2004
# 6.20


# PERF: 7. Write a SQL query to list all movies released in 2010 and their ratings, in descending order by rating. For movies with the same rating, order them alphabetically by title.
def rank_years_movies():
    """Get user input of year and return all the year's movies in
    order by rating. For movies with the same rating, order them alphabetically."""

    year = get_year()

    sql = "SELECT movies.title, ratings.rating FROM movies " \
        "JOIN ratings ON movies.id = ratings.movie_id " \
        "WHERE movies.year = ? " \
        "ORDER BY ratings.rating ASC, movies.title"

    ranked = db.execute(sql, year)
    for movie in ranked:
        print(movie['title'], movie['rating'])



# NOTE: Uncomment to run in main()
# rank_years_movies()


# PERF: 8. Write a SQL query to list the names of all people who starred in Toy Story.
def stars_of_movie():
    """Get user input of a movie and return the names of all people
    who starred in that movie."""

    title = get_movie()

    sql = "SELECT name FROM people WHERE id IN " \
        "(SELECT person_id FROM stars WHERE movie_id IN " \
        " (SELECT id FROM movies WHERE title = ?))"

    stars = db.execute(sql, title)
    for person in stars:
        print(person['name'])


# NOTE: Uncomment to run in main()
# stars_of_movie()
# ❯ py movies.py
# Title: Titanic
# Leonardo DiCaprio
# Kate Winslet
# Billy Zane
# Kathy Bates
# .....etc.


# # PERF: 9. Write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
def sort_year_stars_by_age():
    """Get user input of year and return all stars of movies of that year by age."""

    year = get_year()

    sql = "SELECT name FROM people WHERE id IN " \
        "(SELECT DISTINCT person_id FROM stars WHERE movie_id IN " \
        "(SELECT id FROM movies WHERE year = ?)) ORDER BY birth"

    stars = db.execute(sql, year)
    for person in stars:
        print(person['name'])


# NOTE: Uncomment to run in main()
# sort_year_stars_by_age()


# PERF: 10. Write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.
def dir_min9():
    """List the names of all people who have directed a movie that
    received a rating of at least 9.0."""

    sql = "SELECT name FROM people WHERE id IN " \
        "(SELECT person_id FROM directors where movie_id IN" \
        "(SELECT movie_id FROM ratings WHERE rating >= 9))"

    good_directors = db.execute(sql)

    for director in good_directors:
        print(director['name'])


# NOTE: Uncomment to run in main()
# dir_min9()


# PERF: 11. Write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
def top5():
    """Get user input for an actor and return five highest rated
    movies that actor starred in."""

    actor = input("Actor: ")

    sql = "SELECT movies.title FROM movies " \
        "JOIN stars ON stars.movie_id = movies.id " \
        "JOIN ratings ON ratings.movie_id = movies.id " \
        "JOIN people ON stars.person_id = people.id " \
        "WHERE people.name = ? " \
        "ORDER by ratings.rating DESC LIMIT 5"

    top = db.execute(sql, actor)
    print(top)


# NOTE: Uncomment to run in main()
# top5()


# NOTE: 12. Write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
def costars():
    """Get input from user for two actors and list all movies in which they
    costarred."""

    act1 = input("Actor 1: ")
    act2 = input("Actor 2: ")

    sql = """SELECT title FROM movies
        JOIN stars ON movies.id = stars.movie_id
        JOIN people ON stars.person_id = people.id
        WHERE name = ?
            AND movies.title IN
            (SELECT title FROM movies
                JOIN stars ON movies.id = stars.movie_id
                JOIN people ON stars.person_id = people.id
            WHERE name = ?)"""



    movies = db.execute(sql, act1, act2)
    print(movies)
    try:                          # Alternatively, try `if movies not == []`
        print(movies[0]['title'])
    except IndexError:
        print("No shared movie found.")


# NOTE: Uncomment to run in main()
# costars()
# ❯ py movies.py
# Actor 1: Tom Cruise
# Actor 2: Brad Pitt
# Interview with the Vampire: The Vampire Chronicles


# NOTE: 13.  Write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
def bacon_number():
    """SQL query to list all people who starred in a movie in which
    Kevin Bacon also starred."""

    sql = """SELECT DISTINCT name FROM people
                JOIN stars ON people.id = stars.person_id
                JOIN movies ON stars.movie_id = movies.id
            WHERE movies.title IN
                (SELECT title FROM movies
                    JOIN stars ON movies.id = stars.movie_id
                    JOIN people ON stars.person_id = people.id
                WHERE name = "Kevin Bacon" AND birth = 1958)"""

    bacon_costars = db.execute(sql)

    print(bacon_costars)


bacon_number()
