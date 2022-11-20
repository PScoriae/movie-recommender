import requests
from requests.utils import requote_uri
from dotenv import load_dotenv
import os

load_dotenv()
tmdbApiKey = os.environ["TMDB_API_KEY"]

print(
    """
Welcome to the Movie Recommender!
Please enter a semi-colon delimited (;) list of movies that you like and then hit enter.

For example:
top gun; joker; baby driver

Using the list, I will recommend you movies that you will probably like based on criteria
such as actor, genre, director and company.
""")


# takes semi-colon delimited string of movies and returns a
# url encoded list of strings for API call
def processUserInput(userInput):
    movieList = userInput.split(";")

    # 10
    # remove trailing whitespace
    strippedMovieList = [x.strip() for x in movieList]
    # alternative
    # 6 and 9
    # strippedMovieList = list(map(lambda movie: movie.strip(), movieList))

    # 6 and 9
    return list(map(lambda movie: requote_uri(movie), strippedMovieList))


# 2
getMovieList = processUserInput


# 4
def forMovies(funcGetMovieList):

    # 6 and 9
    # response returns list of objects matching search criteria
    def callTmdbApi(tmdbApiKey):
        return list(map(lambda movieName: requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={tmdbApiKey}&language=en-US&query={movieName}&page=1&include_adult=false").json(), funcGetMovieList(input())))

    # 5
    return callTmdbApi


# 5
def untilNthMovie(n):
    def getNthMovieOnly(obj):
        return obj["results"][:n+1]
    return getNthMovieOnly


# 4
def getMostPopularMovies(moviesInfos, filterFunc):
    return list(map(filterFunc, moviesInfos))


# 2
getMoviesInfos = forMovies(getMovieList)

# 2
moviesInfos = getMoviesInfos(tmdbApiKey)

# 2
getFirstMovieOnly = untilNthMovie(0)


movieList = getMostPopularMovies(moviesInfos, getFirstMovieOnly)
