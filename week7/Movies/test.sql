SELECT title FROM movies
    JOIN stars ON movies.id = stars.movie_id
    JOIN people ON stars.person_id = people.id
    WHERE name = 'Helena Bonham Carter'
        AND movies.title IN
        (SELECT title FROM movies
            JOIN stars ON movies.id = stars.movie_id
            JOIN people ON stars.person_id = people.id
            WHERE name = 'Johnny Depp')


SELECT DISTINCT name FROM people
        JOIN stars ON people.id = stars.person_id
        JOIN movies ON stars.movie_id = movies.id
    WHERE title IN
        (SELECT title FROM movies
            JOIN stars ON movies.id = stars.movie_id
            JOIN people ON stars.person_id = people.id
        WHERE name = "Kevin Bacon" AND birth = 1958);
