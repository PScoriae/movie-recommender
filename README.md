<div align='center'>

# Movie Recommender

<p>
  <a href="https://linkedin.com/in/pierreccesario">
    <img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555">
  </a>
  <a href="https://github.com/PScoriae/movie-recommender/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-WTFPL-brightgreen?style=for-the-badge">
  </a>
</p>

</div>

# About

This simple Python3 CLI program returns 3 recommended movies based on a list of favorite movies that the user provides.

Various criteria from the user's favorite movies such as director, genre and cast are used to determine the 3 recommended movies.

All data is collected from [The Movie Database](https://www.themoviedb.org)'s API.

This program was made to demonstrate the use of 11 functional programming concepts, namely:

- Separating functions and data
- Assigning a function to a variable
- Create a list of functions and use that list
- Passing functions as arguments
- Returning functions
- Mapping
- Filtering
- Reducing
- Lambdas
- List Comprehensions
- Recursion

In `main.py`, these 11 concepts are labelled from 1 to 11 and are referenced each time they are used.

# Prerequisites

You'll need to install **Python3** on your system to run this program. Consult the [official website](https://www.python.org/downloads/) for installation instructions.

# Installation

1.  First, `git clone` this repository,

        git clone https://github.com/PScoriae/movie-recommender

2.  Then, add a `.env` file to the root directory of the project for your TMDB API key. You may refer to [`.env.example`](.env.example).

# Running the Program

First, open a terminal in the project's root directory. Then, `cd` into the `src` folder like so:

    cd src

Finally, run the following command:

    python3 main.py
