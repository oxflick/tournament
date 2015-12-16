DROP DATABASE IF EXISTS tournament;
-- Create database

CREATE DATABASE tournament;
-- Connect to the database
\c tournament

-- Drop all tables and views if they exist
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS match_records CASCADE;
DROP VIEW IF EXISTS wins CASCADE;
DROP VIEW IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS standings CASCADE;

CREATE TABLE players ( name TEXT,
                     id SERIAL primary key
                     );

CREATE TABLE match_records ( loser INTEGER references players(id),
                           winner INTEGER references players(id),
                           id SERIAL primary key
                           );

-- View to show number of wins for each Player
CREATE VIEW wins AS
SELECT
players.id,
count(match_records.winner) as num
FROM players LEFT JOIN match_records
ON players.id = match_records.winner
GROUP BY players.id;

-- View to show number of matches for each Player
CREATE VIEW matches AS
SELECT players.id, COUNT(match_records.id) AS num 
FROM players
LEFT JOIN match_records
ON players.id = match_records.winner OR players.id = match_records.loser
GROUP BY players.id;                               

-- View to show number of wins and matches for each Player
CREATE VIEW standings AS 
SELECT players.id, players.name, wins.num AS wins, matches.num AS matches 
FROM players, matches, wins
WHERE players.id = wins.id AND wins.id = matches.id;


                               


