import sqlite3

def get_connection():
    return sqlite3.connect('notsteam.db')

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
