def read_ratings_data(f: str) -> dict:
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    movie_ratings_dict = {}
    
    with open(f, 'r') as file:
        for line in file:
            rating_info = line.strip().split('|')
            movie_name = rating_info[0]
            rating = float(rating_info[1])

            if movie_name in movie_ratings_dict:
                movie_ratings_dict[movie_name].append(rating)
            else:
                movie_ratings_dict[movie_name] = [rating]

    return movie_ratings_dict

def read_movie_genre(f: str) -> dict:
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    movie_genre_dict = {}

    with open(f,'r') as file:
        for line in file:
            movie_info = line.strip().split('|')
            if len(movie_info) == 3:
                genre, x, movie = movie_info
                genre = genre.strip()
                movie = movie.strip()

                movie_genre_dict[movie] = genre

    return movie_genre_dict

def create_genre_dict(d: dict) -> dict:
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    genre_dict = {}

    for movie, genre in d.items():
        if genre in genre_dict:
            genre_dict[genre].append(movie)
        else:
            genre_dict[genre] = [movie]

    return genre_dict
    
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    avg_rating_dict = {}

    for movie, ratings in d.items():
        avg = sum(ratings) / len(ratings)
        avg_rating_dict[movie] = round(avg, 1)
    
    return avg_rating_dict

def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    popular_movies_dict = {}

    sorted_movies = sorted(d.items(), key=lambda x: x[1], reverse=True)
    n_movies = sorted_movies[:n]

    for movie, rating in n_movies:
        popular_movies_dict[movie] = rating
    
    return popular_movies_dict

def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    filtered_movies_dict = {}

    sorted_movies = sorted(d.items(), key=lambda x: x[1], reverse=True)
    
    for movie, rating in sorted_movies:
        if rating >= thres_rating:
            filtered_movies_dict[movie] = rating

    return filtered_movies_dict

def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    popular_in_genre_dict = {}

    if genre not in genre_to_movies:
        return {}
    
    movies_in_genre = genre_to_movies[genre]

    genre_ratings = {}
    for movie in movies_in_genre:
        if movie in movie_to_average_rating:
            genre_ratings[movie] = movie_to_average_rating[movie]

    sorted_genre_movies = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)

    n_movies = sorted_genre_movies[:n]

    for movie, rating in n_movies:
        popular_in_genre_dict[movie] = rating
    
    return popular_in_genre_dict

def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    movies_in_genre = genre_to_movies[genre]

    genre_ratings = {}
    for movie in movies_in_genre:
        if movie in movie_to_average_rating:
            genre_ratings[movie] = movie_to_average_rating[movie]
    
    if len(genre_ratings) == 0:
        return 0.0 
        
    avg_genre_ratings = sum(genre_ratings.values()) / len(genre_ratings)

    return avg_genre_ratings

def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    avgrating_genre_dict = {}

    for genre in genre_to_movies:
        avg_rating = get_genre_rating(genre, genre_to_movies, movie_to_average_rating)
        avgrating_genre_dict[genre] = avg_rating

    sorted_genre = sorted(avgrating_genre_dict.items(), key=lambda x: -x[1])

    top_genres = {}
    for genre, rating in sorted_genre[:n]:
        top_genres[genre] = rating

    return top_genres

def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    user_to_movies_dict = {}

    with open(f,'r') as file:
        for line in file:
            rating_info = line.strip().split('|')
            movie_name = rating_info[0]
            rating = float(rating_info[1])
            user_id = int(rating_info[2])

            if user_id in user_to_movies_dict:
                user_to_movies_dict[user_id].append((movie_name,rating))
            else:
                user_to_movies_dict[user_id] = [(movie_name,rating)]

    return user_to_movies_dict

def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    genre_ratings = {}
    if user_id not in user_to_movies:
        return None

    user_movies = user_to_movies[user_id]

    for movie, rating in user_movies:
        if movie in movie_to_genre:
            genre = movie_to_genre[movie]  

            if genre not in genre_ratings:
                genre_ratings[genre] = [0, 0]  

            genre_ratings[genre][0] += rating
            genre_ratings[genre][1] += 1

    avg_genre_ratings = {}
    for genre, (total, count) in genre_ratings.items():
        avg_rating = total / count
        avg_genre_ratings[genre] = avg_rating

    if not avg_genre_ratings:
        return None

    top_genre = max(avg_genre_ratings, key=avg_genre_ratings.get)
    
    return top_genre

def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    if not top_genre:
        return {}

    genre_to_movies = create_genre_dict(movie_to_genre)
    if top_genre not in genre_to_movies:
        return {}
    
    movies_in_genre = genre_to_movies[top_genre]

    rated_movies = set()
    if user_id in user_to_movies:
        rated_movies = {movie for movie, _ in user_to_movies[user_id]}

    unrated_movies = [movie for movie in movies_in_genre if movie not in rated_movies]

    unrated_movie_ratings = {}
    for movie in unrated_movies:
        if movie in movie_to_average_rating:
            unrated_movie_ratings[movie] = movie_to_average_rating[movie]

    sorted_movies = sorted(unrated_movie_ratings.items(), key=lambda x: x[1], reverse=True)

    top_3 = sorted_movies[:3]

    result = {}
    for movie, rating in top_3:
        result[movie] = rating

    return result