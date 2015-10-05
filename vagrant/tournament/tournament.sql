-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- We assume that each player has at most 20 games and 20 characters for name


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	id serial primary key,
	name text
);

-- We assume that a new round of matches begins only after current round ends.

CREATE TABLE matches (
	game_id serial,
	winner_id int references players(id),
	loser_id int references players(id)

); 
