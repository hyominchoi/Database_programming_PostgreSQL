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
    conn = connect()
    cur = conn.cursor()
    cur.execute("""UPDATE players SET score = 0;""")
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE FROM players;""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT COUNT (name) FROM players;""")
    result = cur.fetchone()
    conn.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO players (name, score) VALUES (%s, 0);""", [(name)] )
    conn.commit()
    conn.close()


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

    conn = connect()
    cur = conn.cursor()

    standings = []

    # We sort the current position by result score
    cur.execute(""" SELECT id, name, score FROM players ORDER BY score; """)
    for line in cur.fetchall():
        print line 
        id_num = line[0]
        name = line[1]
        score = line[2]
        if score is None:
            score = 0
        wins = (bin(score).count("1"))
        t = (id_num, name, score, wins)
        standings += [t]
    
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cur = conn.cursor()
    
    # We update rscore entry for the winner
    cur.execute ("""SELECT score FROM players WHERE id = %s;""", [winner])
    winner_update = cur.fetchone()[0] * 2 + 1
    cur.execute("""UPDATE players SET score = %s WHERE id = %s ;""", [winner_update, winner])
    
    # We update score entry for the loser
    cur.execute("""SELECT score FROM players WHERE id = '%s';""", [loser])
    loser_update = cur.fetchone()[0] * 2 
    cur.execute("""UPDATE players SET score = %s WHERE id = '%s';""", [loser_update, loser])

    conn.commit()   
    conn.close()

 
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
    # We first want to know how many players there are
    c = countPlayers()

    # We will retur the following paring list in the end
    paring_list = []

    conn = connect()
    cur = conn.cursor()

    # We sort the current position by result score
    cur.execute(""" SELECT id, name FROM players ORDER BY score; """)
    
    # Construct list of tuples
    l = cur.fetchall()
    for i in range(0,c/2):
        paring_list += [l [2 * i] + l[ 2 * i + 1]]

    conn.close()
    return paring_list
