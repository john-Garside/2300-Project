DROP TABLE IF EXISTS Digital;
DROP TABLE IF EXISTS Physical;
DROP TABLE IF EXISTS Belongs_To;
DROP TABLE IF EXISTS Is_Given;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Owns;
DROP TABLE IF EXISTS Wishlist;
DROP TABLE IF EXISTS Achievement;
DROP TABLE IF EXISTS Game; -- order is to respect dependent tables
DROP TABLE IF EXISTS Player; -- user is not used because it is a protected keyword


CREATE TABLE Player (
  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
  playername  TEXT  UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Game (
  game_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT UNIQUE NOT NULL,
  release_date TEXT, -- Do i remove not null for not yet released games
  rating INTEGER DEFAULT 0,
  platform TEXT NOT NULL,
  developer TEXT NOT NULL
);

CREATE TABLE Genre (
  genre_name TEXT PRIMARY KEY-- do I need to make not null?
);

CREATE TABLE Tag (
  tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
