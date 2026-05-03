import sqlite3
import database


def login_menu():
    while True:
        print("\n--- Not Steam ---")
        print("1. Login")
        print("2. Register")
        print("3. Quit")
        choice = input("Choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            player = database.login(username, password)
            if player is None:
                print("Invalid credentials")
            else:
                print("Login successful")
                main_menu(player)
        elif choice == "2":
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")
            try:
                database.add_player(username, email, password)
                print("Player added, please log in")
            except sqlite3.IntegrityError:
                print("Username or email already taken")
        elif choice == "3":
            exit()
        else:
            print("Invalid choice, try again")


def player_owns_game(player_id, game_id):
    # helper: check if a game is in the player's library
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT 1 FROM Owns WHERE player_id = ? AND game_id = ?",
        (player_id, game_id)
    )
    result = cursor.fetchone()
    connection.close()
    return result is not None


def prompt_int(prompt):
    # small helper to safely read an integer from the user
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError:
        print("That wasn't a valid number.")
        return None


def prompt_for_game_id(prompt="Game title: "):
    # ask for a title, look it up, disambiguate if needed; returns a game_id or None
    title = input(prompt)
    matches = database.get_games_by_title(title)
    if not matches:
        print("No game with that title.")
        return None
    if len(matches) == 1:
        return matches[0][0]
    print("Multiple games with that title:")
    for i, (gid, t, dev) in enumerate(matches, start=1):
        print(f"  {i}. {t!r} - {dev}")
    pick = prompt_int("Pick a number: ")
    if pick is None or pick < 1 or pick > len(matches):
        print("Invalid selection.")
        return None
    return matches[pick - 1][0]


def main_menu(player):
    player_id = player[0]
    playername = player[1]

    while True:
        print(f"""
--- Welcome, {playername} ---
1.  View my library
2.  Add a game
3.  Edit a game
4.  Delete a game
5.  Search by title
6.  Search by genre
7.  Search by tag
8.  View wishlist
9.  Add to wishlist
10. Remove from wishlist
11. View achievements
12. Add achievement
13. Assign tag to game
14. Assign genre to game
15. Set game as digital
16. Set game as physical
17. View total playtime
18. Logout
""")
        choice = input("Choice: ")

        match choice:
            case "1":
                # View my library
                library = database.get_player_library(player_id)
                if not library:
                    print("Your library is empty.")
                else:
                    print("\n--- Your Library ---")
                    for title, developer, playtime in library:
                        print(f"- {title} ({developer}) - {playtime} hrs")

            case "2":
                # Add a game
                title = input("Title: ")
                release_date = input("Release date (YYYY-MM-DD): ")
                rating_raw = input("Rating (0-10): ")
                try:
                    rating = int(rating_raw)
                except ValueError:
                    rating = 0
                platform = input("Platform: ")
                developer = input("Developer: ")
                try:
                    new_id = database.add_game(title, release_date, rating, platform, developer)
                    print(f"'{title}' added to catalog.")
                    add_to_lib = input("Add to your library too? (y/n): ")
                    if add_to_lib.strip().lower() == "y":
                        try:
                            database.add_to_library(player_id, new_id)
                            print("Added to your library.")
                        except sqlite3.IntegrityError:
                            print("Couldn't add to library.")
                except sqlite3.IntegrityError:
                    print("A game with that title already exists.")

            case "3":
                # Edit a game (only games in player's library)
                game_id = prompt_for_game_id("Title of game to edit: ")
                if game_id is None:
                    continue
                if not player_owns_game(player_id, game_id):
                    print("You can only edit games in your library.")
                    continue
                column = input("Column to edit (title, release_date, rating, platform, developer): ")
                new_value = input("New value: ")
                try:
                    database.edit_game(game_id, column, new_value)
                    print("Game updated.")
                except ValueError as e:
                    print(e)
                except sqlite3.IntegrityError:
                    print("That update conflicts with an existing record.")

            case "4":
                # Delete a game (only games in player's library)
                game_id = prompt_for_game_id("Title of game to delete: ")
                if game_id is None:
                    continue
                if not player_owns_game(player_id, game_id):
                    print("You can only delete games in your library.")
                    continue
                try:
                    database.delete_game(game_id)
                    print("Game deleted.")
                except sqlite3.IntegrityError:
                    print("Cannot delete - other records depend on this game.")

            case "5":
                # Search by title
                title = input("Title (partial OK): ")
                results = database.search_by_title(title)
                if not results:
                    print("No games found.")
                else:
                    for t, date, rating, platform, dev in results:
                        print(f"- {t} ({date}) - {dev} - {platform} - rating {rating}")

            case "6":
                # Search by genre
                genre = input("Genre name: ")
                results = database.get_games_by_genre(genre)
                if not results:
                    print("No games found in that genre.")
                else:
                    for title, dev in results:
                        print(f"- {title} ({dev})")

            case "7":
                # Search by tag
                tag = input("Tag name: ")
                results = database.get_games_by_tag(tag)
                if not results:
                    print("No games found with that tag.")
                else:
                    for title, dev in results:
                        print(f"- {title} ({dev})")

            case "8":
                # View wishlist
                wishlist = database.get_wishlist(player_id)
                if not wishlist:
                    print("Your wishlist is empty.")
                else:
                    print("\n--- Your Wishlist ---")
                    for title, release_date in wishlist:
                        print(f"- {title} ({release_date})")

            case "9":
                # Add to wishlist
                game_id = prompt_for_game_id("Title of game to add to wishlist: ")
                if game_id is None:
                    continue
                try:
                    database.add_to_wishlist(player_id, game_id)
                    print("Added to wishlist.")
                except sqlite3.IntegrityError:
                    print("Couldn't add - either already on your wishlist or that game doesn't exist.")

            case "10":
                # Remove from wishlist
                game_id = prompt_for_game_id("Title of game to remove from wishlist: ")
                if game_id is None:
                    continue
                database.remove_from_wishlist(player_id, game_id)
                print("Removed from wishlist (if it was there).")

            case "11":
                # View achievements
                game_id = prompt_for_game_id("Title of game to view achievements for: ")
                if game_id is None:
                    continue
                achievements = database.get_achievements(player_id, game_id)
                if not achievements:
                    print("No achievements for that game.")
                else:
                    print("\n--- Achievements ---")
                    for (name,) in achievements:
                        print(f"- {name}")

            case "12":
                # Add achievement
                game_id = prompt_for_game_id("Title of game: ")
                if game_id is None:
                    continue
                name = input("Achievement name: ")
                try:
                    database.add_achievement(player_id, game_id, name)
                    print(f"Achievement '{name}' earned!")
                except sqlite3.IntegrityError:
                    print("Couldn't add achievement - that game might not exist.")

            case "13":
                # Assign tag to game
                game_id = prompt_for_game_id("Title of game: ")
                if game_id is None:
                    continue
                tag_name = input("Tag name: ")
                try:
                    database.assign_tag(game_id, tag_name)
                    print(f"Tag '{tag_name}' assigned.")
                except sqlite3.IntegrityError:
                    print("Couldn't assign tag - that game might not exist.")

            case "14":
                # Assign genre to game
                game_id = prompt_for_game_id("Title of game: ")
                if game_id is None:
                    continue
                genre_name = input("Genre name: ")
                try:
                    database.assign_genre(game_id, genre_name)
                    print(f"Genre '{genre_name}' assigned.")
                except sqlite3.IntegrityError:
                    print("Couldn't assign genre - that game might not exist or already has it.")

            case "15":
                # Set game as digital
                game_id = prompt_for_game_id("Title of game: ")
                if game_id is None:
                    continue
                file_size_raw = input("File size (in GB or whatever unit you use): ")
                try:
                    file_size = int(file_size_raw)
                except ValueError:
                    print("Invalid file size.")
                    continue
                store_link = input("Store link: ")
                try:
                    database.set_digital(game_id, file_size, store_link)
                    print("Game set as digital.")
                except sqlite3.IntegrityError:
                    print("Couldn't set - that game might not exist.")

            case "16":
                # Set game as physical
                game_id = prompt_for_game_id("Title of game: ")
                if game_id is None:
                    continue
                condition = input("Condition (e.g. great, good, bad): ")
                shelf_location = input("Shelf location: ")
                try:
                    database.set_physical(game_id, condition, shelf_location)
                    print("Game set as physical.")
                except sqlite3.IntegrityError:
                    print("Couldn't set - that game might not exist.")

            case "17":
                # View total playtime
                results = database.get_total_playtime(player_id)
                if not results:
                    print("No playtime recorded.")
                else:
                    for name, total in results:
                        print(f"{name} has played {total} hours total.")

            case "18":
                print("Logging out...")
                return

            case _:
                print("Invalid choice, try again")


if __name__ == "__main__":
    login_menu()
