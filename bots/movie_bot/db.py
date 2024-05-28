import sqlite3
from random import sample


def get_movies_list(tablename: str, counts_movies: int) -> list[tuple[str]]:
    conn = sqlite3.connect('movies.db')
    movies = conn.execute(f'SELECT title, link FROM {tablename};').fetchall()
    conn.close()
    select_movies = sample(movies, k=counts_movies)
    return select_movies
