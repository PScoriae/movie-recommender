import requests
from requests.utils import requote_uri
from dotenv import load_dotenv
import os
from functools import reduce

load_dotenv()
tmdbApiKey = os.environ["TMDB_API_KEY"]

print(
    """
Welcome to the Movie Recommender!
Please enter a semi-colon delimited (;) list of movies that you like and then hit enter.

For example:
top gun; joker; baby driver

Using the list, I will recommend you movies that you will probably like based on criteria
such as actor, genre and director.
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


# 5
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

    # 7
    directorList = list(filter(lambda x: x['job'] == "Director", crewList))
    for director in directorList:
        directorNames.append(director['id'])
    return directorNames


def queryRecByGenre(tmdbApiKey, genreList):
    tmp = list(map(lambda x: str(x), genreList))
    genreListString = ", ".join(tmp)
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={requote_uri(genreListString)}&with_watch_monetization_types=flatrate").json()
    if res['total_results'] == 0:
        queryRecByGenre(tmdbApiKey, list(genreList)[:len(genreList)-1])
    return res['results'][:3]


def queryRecByLeadActor(tmdbApiKey, leadActor):
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_cast={leadActor}&with_watch_monetization_types=flatrate").json()
    return res['results'][:3]


def queryRecByDirector(tmdbApiKey, director):
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_crew={director}&with_watch_monetization_types=flatrate").json()
    return res['results'][:3]


def baseFilter(unwantedMovieIds):
    def notSearched(movieObj):
        return movieObj['id'] not in unwantedMovieIds
    return notSearched


def getUniqueMovieList(movieList):
    tmp = []
    for movie in movieList:
        if movie not in tmp:
            tmp.append(movie)
    return tmp


# 2
getMoviesInfos = forMovies(processUserInput)

# 2
moviesInfos = getMoviesInfos(tmdbApiKey)

# 2
getFirstMovieOnly = untilNthMovie(0)

movieInfoList = filterTopResults(moviesInfos, getFirstMovieOnly)

moviesGenresIds = list(map(getGenreMovieId, movieInfoList))

searchedMovieIds = [int(x['id']) for x in movieInfoList]

# 6 and 9
genreIds = list(map(lambda x: x['genreIds'], moviesGenresIds))

# 10
flattenedGenreIds = set(reduce(lambda a, b: a+b, genreIds))

credits = list(map(getCastCrew, moviesGenresIds))

getLeadCast = untilNthCast(1, "cast")

castList = filterTopResults(credits, getLeadCast)

castIds = list(map(getCastId, castList))

flattenedCastIds = set(reduce(lambda a, b: a+b, castIds))

directorList = list(map(getDirector, credits))

flattenedDirectorsIds = set(reduce(lambda a, b: a+b, directorList))

top3MoviesByGenre = queryRecByGenre(tmdbApiKey, flattenedGenreIds)
topMoviesByLeadActor = list(queryRecByLeadActor(tmdbApiKey, x)
                            for x in flattenedCastIds)
flattenedTopMoviesByLeadActor = [
    item for sublist in topMoviesByLeadActor for item in sublist]
topMoviesByDirector = list(queryRecByDirector(tmdbApiKey, x)
                           for x in flattenedDirectorsIds)
flattenedTopMoviesByDirector = [
    item for sublist in topMoviesByDirector for item in sublist]

combinedMovieList = [*top3MoviesByGenre, *
                     flattenedTopMoviesByDirector, *flattenedTopMoviesByDirector]


filterMovieList = baseFilter(searchedMovieIds)

filteredCombinedMovieList = list(
    filter(filterMovieList, combinedMovieList))

sortedMovieList = sorted(filteredCombinedMovieList,
                         key=lambda x: x['popularity'], reverse=True)

formattedMovieList = list(
    map(lambda x: [x['original_title'], x['overview']], sortedMovieList))


uniqueMovieList = getUniqueMovieList(formattedMovieList)

top3Movies = uniqueMovieList[:3]


print(
    f"""
Your top 3 recommended movies are:
1. {top3Movies[0][0]}
Overview: {top3Movies[0][1]}

2. {top3Movies[1][0]}
Overview: {top3Movies[1][1]}

3. {top3Movies[2][0]}
Overview: {top3Movies[2][1]}
"""
)
