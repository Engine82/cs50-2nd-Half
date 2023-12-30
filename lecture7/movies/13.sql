SELECT DISTINCT(name) FROM people, stars, movies
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND movies.id IN(
    SELECT movies.id FROM movies, stars, people
    WHERE movies.id = stars.movie_id
    AND stars.person_id = people.id
    AND people.id IN(
        SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958
    ))
AND people.id NOT IN(
    SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958
);