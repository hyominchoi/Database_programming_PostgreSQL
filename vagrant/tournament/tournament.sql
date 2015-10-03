-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- We assume that each player has at most 20 games and 20 characters for name

-- Results column in players updates the score in a binary way. 
-- I.e. If win, new score = score * 2 + 1, if loose, new score = old score * 2. 
-- This will be done in tournament.py

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	id serial,
	name varchar(20),
	score int
	


CREATE TABLE matches (
	round int,
	game int,
	winner_id int,
	looser_id int

); 
