
DROP DATABASE IF EXISTS tournament;
-- create database
CREATE DATABASE tournament;
-- connect to the database
\c tournament

CREATE TABLE players ( name TEXT,
                     id SERIAL primary key,
                     wins INTEGER DEFAULT 0,
	                 matches INTEGER DEFAULT 0
                     );

CREATE TABLE match_records ( loser INTEGER references players(id),
                           winner INTEGER references players(id),
                           id SERIAL );





                               


