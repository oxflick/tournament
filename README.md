<h1>Project: Tournament Planner </h1>

<li>cd to the repo </li>
<li>run python tournament_test.py </li>

In this project, I wrote a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible.

You’ll find three files in this project: tournament.sql, tournament.py, and tournament_test.py.

The template file tournament.sql has the database schema, in the form of SQL create table commands. 

The template file tournament.py has a Python module. In this file there are several functions. Each function has a docstring that says what it does.

Finally, the file tournament_test.py contains unit tests that tests the functions I've written in tournament.py. 