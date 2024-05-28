def get_genre(selected_genre: str, genres: dict[str, str]) -> str:
    for genre in genres:
        if selected_genre == genres[genre]:
            return genre


def generate_message_with_movies_list(movies_list: list[tuple[str]]) -> str:
    movies = ''
    for movie in movies_list:
        movies += f'- <a href="{movie[1]}">{movie[0]}</a>\n'
    return movies
