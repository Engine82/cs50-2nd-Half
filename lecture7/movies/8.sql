SELECT name FROM people, stars
WHERE stars.movie_id IN (SELECT id FROM movies WHERE title = 'Toy Story')
AND stars.person_id = people.id;