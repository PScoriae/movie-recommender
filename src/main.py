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

    # 10
    def stripList(movieList):
        return [x.strip() for x in movieList]

    # 6 and 9
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
        return obj["results"][n]  # TODO fix to use [:n+1]
    return getNthMovieOnly


def untilNthCast(n, key):
    def getNthCastOnly(obj):
        return obj[key][:n]
    return getNthCastOnly


# 4
def filterTopResults(data, filterFunc):
    return list(map(filterFunc, data))


def getGenreMovieId(obj):
    return {'movieId': obj['id'], 'genreIds': obj['genre_ids']}


def getCastCrew(moviesGenresIdsObj):
    return requests.get(f"https://api.themoviedb.org/3/movie/{moviesGenresIdsObj['movieId']}/credits?api_key={tmdbApiKey}&language=en-US").json()


def getCastId(movieCastList):
    return list(map(lambda x: x['id'], movieCastList))


def getDirector(obj):
    directorNames = []
    crewList = obj['crew']
    directorList = list(filter(lambda x: x['job'] == "Director", crewList))
    for director in directorList:
        directorNames.append(director['id'])
    return directorNames


def getRecommendations(genres, cast, directors):
    requests.get(f"")


# 2
getMoviesInfos = forMovies(processUserInput)

# 2
moviesInfos = getMoviesInfos(tmdbApiKey)

# 2
getFirstMovieOnly = untilNthMovie(0)

movieInfoList = filterTopResults(moviesInfos, getFirstMovieOnly)

moviesGenresIds = list(map(getGenreMovieId, movieInfoList))

# 6 and 9
genreIds = list(map(lambda x: x['genreIds'], moviesGenresIds))

# 10
flattenedGenreIds = set([item for sublist in genreIds for item in sublist])

credits = list(map(getCastCrew, moviesGenresIds))

getFirstFiveCast = untilNthCast(1, "cast")

castList = filterTopResults(credits, getFirstFiveCast)

castIds = list(map(getCastId, castList))

flattenedCastIds = set([item for sublist in castIds for item in sublist])

directorList = list(map(getDirector, credits))

flattenedDirectorsIds = set(
    [item for sublist in directorList for item in sublist])

print(flattenedGenreIds)
print(flattenedCastIds)
print(flattenedDirectorsIds)
