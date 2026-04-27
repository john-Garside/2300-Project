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

--- sample data to insert 

INSERT INTO Player (playername, email, password)
VALUES 
  ('John', 'john@email', 'johnpass'),
  ('Maddox', 'maddox@email', 'maddoxpass'),
  ('Zach', 'zach@email', 'zachpass');

INSERT INTO Game (title, release_date, rating, platform, developer)
VALUES
('Elden Ring',       '2022-02-25', 8,  'PC',  'FromSoftware'),
('Hollow Knight',    '2017-02-24', 9,  'PC',  'Team Cherry'),
('Celeste',          '2018-01-25', 9,  'PC',  'Maddy Thorson'),
('Hades',            '2020-09-17', 10, 'PC',  'Supergiant'),
('Stardew Valley',   '2016-02-26', 9,  'PC',  'ConcernedApe'),
('Doom Eternal',     '2020-03-20', 8,  'PC',  'id Software'),
('Disco Elysium',    '2019-10-15', 10, 'PC',  'ZA/UM'),
('Dark Souls III',   '2016-04-12', 9,  'PC',  'FromSoftware'),
('Cuphead',          '2017-09-29', 8,  'PC',  'Studio MDHR'),
('Outer Wilds',      '2019-05-28', 10, 'PC',  'Mobius Digital');

INSERT INTO Genre (genre_name)
VALUES
  ('FPS'),
  ('Looter shooter'),
  ('souls like'),
  ('farming'),
  ('platformer'),
  ('story rich'),
  ('RPG'),
  ('roguelike');

INSERT INTO Tag (name)
VALUES
  ('fun'),
  ('casual'),
  ('competitive'),
  ('not fun');

INSERT INTO Owns(player_id, game_id, playtime)
VALUES
  (1, 1, 439),
  (1, 2, 22),
  (1, 3, 4000),
  (2, 1, 444),
  (2, 5, 2),
  (2, 9, 12),
  (3, 1, 500),
  (3, 10, 12),
  (3, 7, 400);

INSERT INTO Wishlists(player_id, game_id)
VALUES
  (1, 4),
  (1, 5),
  (1, 6),
  (2, 2),
  (2, 3),
  (2, 4),
  (3, 3),
  (3, 9),
  (3, 6);

INSERT INTO Achievement (player_id, game_id, name, earned)
VALUES
    (1, 1, 'First Boss Defeated', 1),
    (1, 1, 'Elden Lord', 0),
    (1, 2, 'Wings of Steel', 1),
    (1, 3, 'Summit Reached', 1),
    (2, 1, 'First Boss Defeated', 1),
    (2, 5, 'Master Farmer', 1),
    (2, 5, 'Community Hero', 0),
    (3, 1, 'First Boss Defeated', 1),
    (3, 10, 'Nomai Scholar', 1),
    (3, 7, 'True Detective', 0);

INSERT INTO Belongs_To (genre_name, game_id)
VALUES
  ('RPG', 1),
  ('souls like', 2),
  ('platformer', 3),
  ('souls like', 1),
  ('roguelike', 4),
  ('farming', 5),
  ('FPS', 6),
  ('souls like', 8),
  ('platformer', 9),
  ('story rich', 10),
  ('story rich', 7);

INSERT INTO Is_Given (tag_id, game_id)
VALUES
    (1, 1),
    (1, 2),
    (1, 8),
    (2, 5),
    (2, 3),
    (3, 4),
    (3, 6),
    (4, 7),
    (4, 10),
    (1, 9);

INSERT INTO Physical (game_id, condition, shelf_location)
VALUES
  (1, 'bad', 'top shelf'),
  (2, 'good', 'bottom shelf'),
  (3, 'great', 'middle shelf');

INSERT INTO Digital (game_id, file_size, store_link)
VALUES
  (4, 128, 'steam'),
  (5, 300, 'steam'),
  (6, 580, 'steam');
