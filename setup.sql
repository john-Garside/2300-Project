-- GROUP PROJECT with Maddox Reed, Zachary Pipes, John Garside
-- any "user"" in the logical database design diagram
-- is replaced with the word player because user is a protectec keyword

DROP TABLE IF EXISTS Digital;
DROP TABLE IF EXISTS Physical;
DROP TABLE IF EXISTS Belongs_To;
DROP TABLE IF EXISTS Is_Given;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Owns;
DROP TABLE IF EXISTS Wishlists;
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

CREATE TABLE Owns (
  player_id INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  playtime INTEGER DEFAULT 0,
  PRIMARY KEY(player_id, game_id)
  FOREIGN KEY(player_id) REFERENCES Player(player_id),
  FOREIGN KEY(game_id) REFERENCES Game(game_id)
);

CREATE TABLE Wishlists(
  player_id INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  PRIMARY KEY(player_id, game_id),
  FOREIGN KEY(player_id) REFERENCES Player(player_id),
  FOREIGN KEY(game_id) REFERENCES Game(game_id)
);

CREATE TABLE Achievement(
  player_id INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  name TEXT NOT NULL, -- I have decided to make Achievement text mandatory
  earned INTEGER DEFAULT 0, -- sqlite doesnt have bool data type :(
  PRIMARY KEY(player_id, game_id, name), 
  FOREIGN KEY (player_id) REFERENCES Player(player_id),
  FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

CREATE TABLE Belongs_To(
  genre_name TEXT NOT NULL,
  game_id INTEGER NOT NULL,
  PRIMARY KEY(genre_name, game_id),
  FOREIGN KEY (genre_name) REFERENCES Genre(genre_name),
  FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

CREATE TABLE Is_Given(
  tag_id INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  PRIMARY KEY(tag_id, game_id),
  FOREIGN KEY(tag_id) REFERENCES Tag(tag_id),
  FOREIGN KEY(game_id) REFERENCES Game(game_id)
);

CREATE TABLE Physical(
  game_id INTEGER PRIMARY KEY,
  condition TEXT,
  shelf_location TEXT,
  FOREIGN KEY(game_id) REFERENCES Game(game_id)
);

CREATE TABLE Digital(
  game_id INTEGER PRIMARY KEY,
  file_size INTEGER,
  store_link TEXT,
  FOREIGN KEY(game_id) REFERENCES Game(game_id)
);

