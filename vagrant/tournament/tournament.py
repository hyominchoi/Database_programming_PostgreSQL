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
    cur.execute("""DELETE FROM matches;""")
    conn.commit()
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
    cur.execute("""SELECT COUNT (id) FROM players;""")
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
    cur.execute("""INSERT INTO players (name) VALUES (%s);""", [(name)])
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
    
    # We construct and return this list in the end
    standings = []

    # We sort the current position by result:
    # the table y order the player rankings according to their wins 
    # and positions decided byt first_won_game in the tournament graph
    # the tabe z counts each player's loses
    # lastly we join y and z on the player id's
    cur.execute(""" SELECT * FROM wins_and_matches; """)
    for line in cur.fetchall():
        standings += [line]
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
    # We insert a new row to "matches" table
    cur.execute("""INSERT INTO matches (winner_id, loser_id) VALUES ('%s', '%s');""", [winner, loser])
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
    conn = connect()
    cur = conn.cursor()

    # We will retur the following paring list in the end
    pairing_list = []

    # Construct list of tuples
    l = playerStandings()
    bye_player = tuple()
    num_player = len(l)

    # We need to consider the where there is an odd number of players.
    # free_won is a dictionary that represents set of players who has
    # won a free game "bye"
    if (num_player % 2 is 1):
        free_won = {}
        cur.execute(""" SELECT winner_id FROM matches WHERE loser_id IS NULL;""")
        for num in cur.fetchall():
            free_won[num] = 'yes'
        # We need to decide to which player we want to give a next bye
        for i in range(0, num_player):
            current_player = l[i]
            # If current player's id is not in the dictionary,
            # then we give the player a free win
            if (current_player[0] not in free_won.key()):
                bye_player = current_player
                break
        # We need to remove this player from the list of playerStandings
        # for the pairing purpose.
        del l[i]
        # We record the bye match record for this player
        cur.execute("""INSERT INTO matches (winner_id) VALUES ('%s');""", [bye_player[0]])
        conn.commit()

    # We can now pair the players for the next round
    for i in range(0, len(l)/2):
        first_player_info = l[2 * i]
        second_player_info = l[2 * i + 1]
        # Create a tuple of (id1, name1, id2, name2)
        t = (first_player_info[0], first_player_info[1],
             second_player_info[0], second_player_info[1])
        # Concatenate it to the pairing list
        pairing_list += [t]
    conn.close()
    return pairing_list
