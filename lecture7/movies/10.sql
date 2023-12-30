SELECT name FROM people
WHERE id in (SELECT DISTINCT(directors.person_id) FROM directors, ratings
WHERE ratings.rating >= 9.0
AND directors.movie_id = ratings.movie_id);