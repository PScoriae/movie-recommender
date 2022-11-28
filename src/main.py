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

    # 7 and 9
    def removeEmptyStrings(movieList):
        return list(filter(lambda x: x != "", movieList))

    # 6 and 9
    def uriEncodeStrings(strippedMovieList):
        return list(map(lambda movie: requote_uri(movie), strippedMovieList))

    # do not modify original input
    processedList = userInput

    # 3
    actions = [splitInput, stripList, removeEmptyStrings, uriEncodeStrings]

    for action in actions:
        processedList = action(processedList)
    return processedList


# 4
def forMovies(funcGetMovieList):

    # 6 and 9
    # response returns list of objects matching search criteria
    def callTmdbApi(tmdbApiKey):
        return list(map(lambda movieName: requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={tmdbApiKey}&language=en-US&query={movieName}&page=1&include_adult=false").json(),
            funcGetMovieList(input())))

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


def getDirectorIds(obj):
    crewList = obj['crew']

    # 7 and 9
    directorList = list(filter(lambda x: x['job'] == "Director", crewList))
    # 10
    return [director['id'] for director in directorList]


def queryRecByGenre(tmdbApiKey, genreList, max):
    # 10
    tmp = [str(x) for x in genreList]
    genreListString = ", ".join(tmp)
    res = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?api_key={tmdbApiKey}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={requote_uri(genreListString)}&with_watch_monetization_types=flatrate").json()
    if res['total_results'] == 0:
        # 11
        queryRecByGenre(tmdbApiKey, genreList[:len(genreList)-1], max)
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


# 6 and 8
def flatten2DList(myList, setFlag):
    flattenedList = reduce(lambda a, b: a+b, myList)
    if setFlag == 1:
        return set(flattenedList)
    elif setFlag == 0:
        return list(flattenedList)


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
flattenedGenreIds = flatten2DList(genreIds, 1)

# 4 and 6
credits = list(map(getCastCrew, moviesGenresIds))

# 2
getLeadCast = untilNthElement(1, "cast")

# 4 and 6
castList = list(map(getLeadCast, credits))

# 4 and 6
castIds = list(map(getCastId, castList))

flattenedCastIds = flatten2DList(castIds, 1)

# 4 and 6
directorIdList = list(map(getDirectorIds, credits))

flattenedDirectorsIds = flatten2DList(directorIdList, 1)

topMoviesByGenre = queryRecByGenre(tmdbApiKey, flattenedGenreIds, 3)

# 10
topMoviesByLeadActor = [queryRecByPerson(
    tmdbApiKey, "cast", x, 3) for x in flattenedCastIds]

flattenedTopMoviesByLeadActor = flatten2DList(topMoviesByLeadActor, 0)

# 10
topMoviesByDirector = [queryRecByPerson(tmdbApiKey, "crew", x, 3)
                       for x in flattenedDirectorsIds]

flattenedTopMoviesByDirector = flatten2DList(topMoviesByDirector, 0)

# use spread operator to combine all lists into a single list
combinedMovieList = [*topMoviesByGenre, *
                     flattenedTopMoviesByDirector, *flattenedTopMoviesByDirector]

# 2
getUniqueMovieIds = baseFilter(searchedMovieIds)

# 4 and 7
filteredCombinedMovieList = list(
    filter(getUniqueMovieIds, combinedMovieList))

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
