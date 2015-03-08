-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players;
CREATE TABLE players (
    id serial PRIMARY KEY,
    name text
);

DROP TABLE IF EXISTS tournament;
CREATE TABLE tournament (
    id serial PRIMARY KEY,
    winner integer REFERENCES players (id)
);

DROP TABLE IF EXISTS matches;
CREATE TABLE IF NOT EXISTS matches (
    id serial PRIMARY KEY,
    player1_id integer REFERENCES players(id),
    player2_id integer REFERENCES players(id),
    winner integer REFERENCES players(id)
);

DROP VIEW IF EXISTS total_wins;
CREATE VIEW total_wins AS
    SELECT players.id, count(winner) AS wins 
    FROM players LEFT JOIN matches ON players.id = winner
    GROUP BY players.id
;

DROP VIEW IF EXISTS total_matches;
CREATE VIEW total_matches AS
    SELECT players.id, count(matches.id) AS total_matches
    FROM players LEFT JOIN matches
    ON players.id = player1_id or players.id = player2_id
    GROUP BY players.id
;

