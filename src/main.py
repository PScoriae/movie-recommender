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
    def splitInput(text):
        return text.split(";")

    def stripList(movieList):
        return [x.strip() for x in movieList]

    def uriEncodeStrings(strippedMovieList):
        return list(map(lambda movie: requote_uri(movie), strippedMovieList))

    # do not modify original input
    processedList = userInput

    # 3
    actions = [splitInput, stripList, uriEncodeStrings]

    for action in actions:
        processedList = action(processedList)
    return processedList


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
# constructor for making functions that return
# movie results until the nth element
def untilNthMovie(n):
    def getNthMovieOnly(obj):
        return obj["results"][:n+1]
    return getNthMovieOnly


# 4
def getMostPopularMovies(moviesInfos, filterFunc):
    return list(map(filterFunc, moviesInfos))


# 2
getMoviesInfos = forMovies(processUserInput)

# 2
moviesInfos = getMoviesInfos(tmdbApiKey)

# 2
getFirstMovieOnly = untilNthMovie(0)


movieList = getMostPopularMovies(moviesInfos, getFirstMovieOnly)

print(movieList)
