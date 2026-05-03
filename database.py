import sqlite3

def get_connection():
    connection = sqlite3.connect('notsteam.db', isolation_level=None, timeout=5) # had to be changed because 
    cursor = connection.cursor() # the database kept throwing errors with multiple connections at the same time
    cursor.execute("PRAGMA foreign_keys = ON") # database became "locked" this hsould fix it
    return connection # this creates a connection
#however for some reason the way sqlite works requires us to explicitly
#turn on the fk restrictions


def get_all_games():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Game")
    results = cursor.fetchall()
    connection.close()
    return results

def get_games_by_genre(genre_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Game.title, Game.developer
FROM Game
JOIN Belongs_To ON Game.game_id = Belongs_To.game_id
WHERE Belongs_To.genre_name = ? """, (genre_name,))
    results = cursor.fetchall()
    connection.close()
    return results

def add_game(title, release_date, rating, platform, developer):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO Game (title, release_date, rating, platform, developer)
    VALUES(?, ?, ?, ?, ?)
           """, (title, release_date, rating, platform, developer))
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id

def delete_game(game_id):
    connection = get_connection()
    cursor = connection.cursor()
    # delete from dependent tables first so the FK constraints don't block us
    cursor.execute("DELETE FROM Owns WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Wishlists WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Achievement WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Belongs_To WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Is_Given WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Physical WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Digital WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM Game WHERE game_id = ?", (game_id,))
    connection.commit() # we use commits when changing the db and fetchall when just fetching data
    connection.close()

def edit_game(game_id, column_name, new_value):
    connection = get_connection()
    cursor = connection.cursor()
    allowed_columns = {"title", "release_date", "rating", "platform", "developer"}
    if column_name not in allowed_columns: # have to do this check because python just
        raise ValueError(f"{column_name} is not an editable column") # directly substitutes with the f string and this could
    cursor.execute(f""" 
                   UPDATE Game
    SET {column_name} = ?
    WHERE game_id = ? """, (new_value, game_id)) # result in some sql injection, I dont know if this will actually be a problem with the way 
                   # we are going to handle the code, but I guess its good practice
    connection.commit()
    connection.close()

def add_to_library(player_id, game_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO Owns (player_id, game_id, playtime)
    VALUES (?, ?, 0)
                   """, (player_id, game_id))
    connection.commit()
    connection.close()

def get_player_library(player_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Game.title, Game.developer, Owns.playtime
FROM Game
JOIN Owns ON Game.game_id = Owns.game_id
WHERE Owns.player_id = ? """, (player_id,))
    results = cursor.fetchall()
    connection.close()
    return results

def get_total_playtime(player_id): # returns the playtime of a player across all games
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Player.playername, SUM(Owns.playtime) AS total_hours
    FROM Owns
    JOIN Player ON Owns.player_id = Player.player_id
    WHERE Owns.player_id = ?
    GROUP BY Player.playername
    """, (player_id,))
    results = cursor.fetchall()
    connection.close()
    return results


def add_player(playername, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO Player (playername, email, password)
    VALUES(?, ?, ?)
           """, (playername, email, password))
    connection.commit()
    connection.close()

def login(playername, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT * FROM Player
    WHERE playername = ?
            AND password = ?
                   """, (playername, password))
    results = cursor.fetchone()
    connection.close()
    return results

def get_game_info(game_id): # maps to view_game_info 
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Game.title, Game.release_date, Game.rating, Game.platform, Game.developer
                   FROM Game
    WHERE game_id = ?
                   """, (game_id,))
    results = cursor.fetchone()
    connection.close()
    return results

def get_games_by_title(title):
    # exact title match; returns list of (game_id, title, developer)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT game_id, title, developer
                   FROM Game
                   WHERE title = ?
                   """, (title,))
    results = cursor.fetchall()
    connection.close()
    return results

def search_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Game.title, Game.release_date, Game.rating, Game.platform, Game.developer
                   FROM Game
    WHERE title LIKE ?
        """, (f"%{title}%",))
    results = cursor.fetchall()
    connection.close()
    return results

def add_to_wishlist(player_id, game_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO Wishlists (player_id, game_id)
    VALUES(?, ?)
           """, (player_id, game_id))
    connection.commit()
    connection.close()

def remove_from_wishlist(player_id, game_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
               DELETE FROM Wishlists WHERE player_id = ? AND game_id = ? """, (player_id, game_id))
    connection.commit()
    connection.close()

def get_wishlist(player_id):
    connection = get_connection()
    cursor = connection.cursor() # not finished but im tired
    cursor.execute("""
                   SELECT Game.title, Game.release_date
    FROM Game
    JOIN Wishlists ON Game.game_id = Wishlists.game_id 
    WHERE player_id = ?
                   """, (player_id,))
    results = cursor.fetchall()
    connection.close()
    return results

def get_games_by_tag(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT Game.title, Game.developer
    FROM Game
    JOIN Is_Given ON Game.game_id = Is_Given.game_id
    JOIN Tag ON Is_Given.tag_id = Tag.tag_id
    WHERE Tag.name = ?
                   """, (name,))
    results = cursor.fetchall()
    connection.close()
    return results

def assign_tag(game_id, tag_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(" INSERT OR IGNORE INTO Tag (name) VALUES (?)", (tag_name,)) 
    cursor.execute("SELECT tag_id FROM Tag WHERE name = ?", (tag_name,))
    tag_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO Is_Given (game_id, tag_id) VALUES (?, ?)", (game_id, tag_id))
    connection.commit()
    connection.close()

def assign_genre(game_id, genre_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO Genre (genre_name) VALUES (?)", (genre_name,))
    cursor.execute("INSERT INTO Belongs_To (genre_name, game_id) VALUES (?, ?)", (genre_name, game_id))
    connection.commit()
    connection.close()

def set_digital(game_id, file_size, store_link):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO Digital (game_id, file_size, store_link) VALUES (?, ?, ?)", (game_id, file_size, store_link))
    connection.commit()
    connection.close()

def set_physical(game_id, condition, shelf_location):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO Physical (game_id, condition, shelf_location) VALUES (?, ?, ?)", (game_id, condition, shelf_location))
    connection.commit()
    connection.close()

def get_achievements(player_id, game_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT Achievement.name
    FROM Achievement
    WHERE Achievement.game_id = ? and Achievement.player_id = ?
    """, (game_id, player_id))
    results = cursor.fetchall()
    connection.close()
    return results

def add_achievement(player_id, game_id, name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT OR REPLACE INTO Achievement (player_id, game_id, name, earned)
    VALUES (?, ?, ?, 1)
                   """, (player_id, game_id, name))
    connection.commit()
    connection.close()
