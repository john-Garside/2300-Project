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

CREATE TABLE 
