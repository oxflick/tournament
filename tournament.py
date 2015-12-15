#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match_records")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    result = int(c.fetchone()[0])
    DB.commit()
    DB.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0) RETURNING id;", (name,))
    DB.commit()
    DB.close()
     

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name, wins, matches FROM players ORDER BY wins DESC")
    standings = c.fetchall()
    DB.commit()
    DB.close()
    return standings
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO match_records(winner, loser) VALUES(%s, %s)",(winner,loser))
    c.execute("UPDATE players SET (matches, wins) = ((matches + 1), (wins + 1)) WHERE id = %s ", (winner,))
    c.execute("UPDATE players SET matches = (matches+1) WHERE id = %s", (loser,))
    DB.commit()
    DB.close()
 

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT a.id AS id1, a.name AS name1, b.id AS id2, b.name AS name2 \
    FROM players AS a INNER JOIN players AS b ON a.wins = b.wins WHERE a.id!=b.id AND \
    (a.id, b.id) not IN (SELECT winner, loser FROM match_records) AND \
    (b.id, a.id) not IN (SELECT winner, loser FROM match_records)")
    result = c.fetchall()
    DB.commit()
    DB.close()
    return result[:len(result)/2]


