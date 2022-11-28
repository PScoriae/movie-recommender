import requests
from requests.utils import requote_uri
from dotenv import load_dotenv
import os
from functools import reduce

# Key for Functional Programming Concepts and Mechanisms
# 1- Separating functions and data
# 2- Assigning a function to a variable
# 3- Create a list of functions and use that list
# 4- Passing functions as arguments
# 5- Returning functions
# 6- Mapping
# 7- Filtering
# 8- Reducing
# 9- Lambdas
# 10- List Comprehensions
# 11- Recursion

# load environment variables for tmdb api key
load_dotenv()
tmdbApiKey = os.environ["TMDB_API_KEY"]


'''
START FUNCTIONS
'''


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
# results until the nth element
def untilNthElement(n, key):
    def getNthElementOnly(obj):
        return obj[key][:n]
    return getNthElementOnly


# 4
def filterResults(data, filterFunc):
    return list(map(filterFunc, data))


def getGenreMovieId(obj):
    return {'movieId': obj['id'], 'genreIds': obj['genre_ids']}


def getCastCrew(moviesGenresIdsObj):
    return requests.get(f"https://api.themoviedb.org/3/movie/{moviesGenresIdsObj['movieId']}/credits?api_key={tmdbApiKey}&language=en-US").json()


# 6 and 9
def getCastId(movieCastList):
    return list(map(lambda x: x['id'], movieCastList))


def getDirector(obj):
    crewList = obj['crew']

    # 7 and 9
    directorList = list(filter(lambda x: x['job'] == "Director", crewList))
    # 10
    return [director['id'] for director in directorList]


def queryRecByGenre(tmdbApiKey, genreList, max):
    # 6 and 9
    tmp = list(map(lambda x: str(x), genreList))
    genreListString = ", ".join(tmp)
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={requote_uri(genreListString)}&with_watch_monetization_types=flatrate").json()
    if res['total_results'] == 0:
        # 11
        queryRecByGenre(tmdbApiKey, list(genreList)[:len(genreList)-1], 3)
    return res['results'][:max]


def queryRecByPerson(tmdbApiKey, personType, person, max):
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_{personType}={person}&with_watch_monetization_types=flatrate").json()
    return res['results'][:max]


# 5
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


'''
START PROCEDURAL STEPS
'''

print(
    """
Welcome to the Movie Recommender!
Please enter a semi-colon delimited (;) list of movies that you like and then hit enter.

For example:
top gun; joker; baby driver

Using the list, I will recommend you movies that you will probably like based on criteria
such as actor, genre and director.
""")

# 2
getMoviesInfos = forMovies(processUserInput)

# 2
moviesInfos = getMoviesInfos(tmdbApiKey)

# 2
getFirstMovieOnly = untilNthElement(1, "results")

# 4 and 6
movieInfoList = list(map(getFirstMovieOnly, moviesInfos))[0]

# 4 and 6
moviesGenresIds = list(map(getGenreMovieId, movieInfoList))

# 10
searchedMovieIds = [int(x['id']) for x in movieInfoList]

# 6 and 9
genreIds = list(map(lambda x: x['genreIds'], moviesGenresIds))

# 8 and 9
flattenedGenreIds = set(reduce(lambda a, b: a+b, genreIds))

# 4 and 6
credits = list(map(getCastCrew, moviesGenresIds))

# 2
getLeadCast = untilNthElement(1, "cast")

# 4 and 6
castList = list(map(getLeadCast, credits))

# 4 and 6
castIds = list(map(getCastId, castList))

# 6 and 8
flattenedCastIds = set(reduce(lambda a, b: a+b, castIds))

# 4 and 6
directorList = list(map(getDirector, credits))

# 8 and 9
flattenedDirectorsIds = set(reduce(lambda a, b: a+b, directorList))

topMoviesByGenre = queryRecByGenre(tmdbApiKey, flattenedGenreIds, 3)

# 10
topMoviesByLeadActor = list(queryRecByPerson(
    tmdbApiKey, "cast", x, 3) for x in flattenedCastIds)

# 10
flattenedTopMoviesByLeadActor = list(
    reduce(lambda a, b: a+b, topMoviesByLeadActor))

# 10
topMoviesByDirector = list(queryRecByPerson(tmdbApiKey, "crew", x, 3)
                           for x in flattenedDirectorsIds)

# 10
flattenedTopMoviesByDirector = list(
    reduce(lambda a, b: a+b, topMoviesByDirector))

combinedMovieList = [*topMoviesByGenre, *
                     flattenedTopMoviesByDirector, *flattenedTopMoviesByDirector]

# 2
filterMovieList = baseFilter(searchedMovieIds)

# 4 and 7
filteredCombinedMovieList = list(
    filter(filterMovieList, combinedMovieList))

# 9
sortedMovieList = sorted(filteredCombinedMovieList,
                         key=lambda x: x['popularity'], reverse=True)

# 6 and 9
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
