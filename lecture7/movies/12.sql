SELECT title FROM movies
WHERE id IN(
    SELECT movies.id FROM movies, stars, people
    WHERE movies.id = stars.movie_id
    AND stars.person_id = people.id
    AND people.name = 'Bradley Cooper'
)
AND id IN(
    SELECT movies.id FROM movies, stars, people
    WHERE movies.id = stars.movie_id
    AND stars.person_id = people.id
    AND people.name = 'Jennifer Lawrence'
);