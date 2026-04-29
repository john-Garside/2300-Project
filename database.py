import sqlite3

def get_connection():
    connection = sqlite3.connect('notsteam.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
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
JOIN Belongs_To ON Game.game_id = Belongs_to.game_id
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
    connection.commit()
    connection.close()

def delete_game(game_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   DELETE FROM Game WHERE game_id = ? """, (game_id,))
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

def
