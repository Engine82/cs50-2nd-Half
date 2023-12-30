SELECT name FROM people
WHERE id IN(SELECT DISTINCT(people.id) FROM people, stars, movies
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND movies.id IN (SELECT movies.id WHERE year = '2004'))
ORDER BY people.birth;