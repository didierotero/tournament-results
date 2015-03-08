#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(fn):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    def wrapper(*args, **kwargs):
	db = psycopg2.connect("dbname=tournament")
        db.autocommit = True
        cursor = db.cursor()
        result = fn(*args, cursor=cursor, **kwargs)
        db.close()
        return result 
    return wrapper
    
@connect
def deleteMatches(cursor=None):
    """Remove all the match records from the database."""
    query = "DELETE FROM matches;"
    cursor.execute(query) 

@connect
def deletePlayers(cursor=None):
    """Remove all the player records from the database."""
    query = "DELETE FROM players;"
    cursor.execute(query)

@connect
def countPlayers(cursor=None):
    """Returns the number of players currently registered."""
    query = "SELECT count(*) FROM players;"
    cursor.execute(query)
    return cursor.fetchone()[0]

@connect
def registerPlayer(name, cursor=None):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player. (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES(%s)"
    cursor.execute(query, (name,))

@connect
def playerStandings(cursor=None):
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
    query = """SELECT players.id, name, wins, total_matches
               FROM players, total_wins, total_matches
               WHERE players.id = total_wins.id AND
                     players.id = total_matches.id
               ORDER BY wins;
            """
    cursor.execute(query)
    return cursor.fetchall()

@connect
def reportMatch(winner, loser, cursor=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = """INSERT INTO matches (player1_id, player2_id, winner)
               VALUES (%s, %s, %s);
            """ 
    cursor.execute(query, (winner, loser, winner))

@connect
def swissPairings(cursor=None):
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
    standings = playerStandings()
    return [(pair[0][0], pair[0][1], pair[1][0], pair[1][1]) for pair in zip(standings[::2],standings[1::2])]

