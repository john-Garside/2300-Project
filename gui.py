import tkinter as tk # this is the library
from tkinter import ttk, messagebox
import sqlite3
import database

root = tk.Tk()
root.title("Not Steam")
root.geometry("900x600")

# center the window on screen
root.update_idletasks() # forces tkinter to compute the window size before we read it 
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

# clean shutdown when the user clicks the X
def on_close(): # makes sure that it closes properly
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)


def show_login():
    #destroys what is currently being shown in the window
    #this is how the whole app works, there is only ever one root window and when navigating between screens we destroy everything
    #that is currently inside and then we rebuild it. 
    for widget in root.winfo_children(): 
        widget.destroy()
    
    frame = tk.Frame(root)
    frame.pack(expand=True) # this centers it vertically

    tk.Label(frame, text="Not Steam", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
#adds the username section
    tk.Label(frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=1, column=1, padx=5, pady=5)
#same thing but for the password
    tk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    status_label = tk.Label(frame, text="", fg="red")
    status_label.grid(row=3, column=0, columnspan=2)

    def try_login(): # we call this becauuse we want input when button is hit not when screen opens
        player = database.login(username_entry.get(), password_entry.get()) #this is how we read inputs
        if player is None:
            status_label.config(text="Invalid credentials")
        else:
            show_main(player)

    def try_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            status_label.config(text="Username and password required", fg="red")
            return
        #we ask for the email in a pop up, because we have 2 fields in the login screen
        from tkinter import simpledialog
        email = simpledialog.askstring("Register", "Email:", parent=root)
        if not email:
            return
        try:
            database.add_player(username, email, password)
            status_label.config(text="Registered, Now log in.", fg="green")
        except sqlite3.IntegrityError: #my old friend
            status_label.config(text="Username or email already taken", fg="red")
        # placeholder for now, not anymore
      #  status_label.config(text="Register not wired up yet")
    # below we pass the function itself, we dont call it so that python doesnt call it immediatly
    tk.Button(frame, text="Login", command=try_login, width=12).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Register", command=try_register, width=12).grid(row=4, column=1, pady=10)

    # let the Enter key submit the form from either field
    username_entry.bind("<Return>", lambda event: try_login())
    password_entry.bind("<Return>", lambda event: try_login())
    username_entry.focus_set()  # cursor starts in the username field

def show_main(player):
    # placeholder so try_login doesn't crash
    # post login layout where we put a dark sidebar on the left
    for widget in root.winfo_children():
        widget.destroy()

    # sidebar on the left
    sidebar = tk.Frame(root, bg="#2c3e50", width=180)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)  # don't let buttons shrink the sidebar
    # content area on the right
    content = tk.Frame(root, bg="white")
    content.pack(side="right", fill="both", expand=True)

    # status bar at the very bottom of the window
    status = tk.Label(root, text="", anchor="w", bg="#ecf0f1", relief="sunken")
    status.pack(side="bottom", fill="x")

    # ----- sidebar contents -----
    tk.Label(sidebar, text=f"Hi, {player[1]}", bg="#2c3e50", fg="white",
             font=("Arial", 12, "bold")).pack(pady=15)

    # each button switches what's shown in the content frame
    buttons = [
        ("My Library",     lambda: show_library(content, status, player)),
        ("Wishlist",       lambda: show_wishlist(content, status, player)),
        ("Search",         lambda: show_search(content, status, player)),
        ("Achievements",   lambda: show_achievements(content, status, player)),
        ("Tags & Genres",  lambda: show_tags_genres(content, status, player)),
        ("Stats",          lambda: show_stats(content, status, player)),
    ]
    for text, cmd in buttons:
        ttk.Button(sidebar, text=text, command=cmd, width=18).pack(pady=2, padx=10) # button issue fix

    # logout at the bottom of the sidebar
    ttk.Button(sidebar, text="Logout", command=show_login, width=18).pack(side="bottom", pady=15) # fixed button issue on my mac
    # show the library by default when they log in
    show_library(content, status, player)


def clear_frame(frame):
    # helper used by every screen to wipe the content area before drawing anythign else
    for widget in frame.winfo_children():
        widget.destroy()


def show_stats(content, status, player):
    # builds the satistics dashboard that shows total playtime, library size, wishlist size, and earned achievements
    # we do not have a function for earned achievments so we just run sql
    clear_frame(content)
    player_id = player[0]

    tk.Label(content, text="Statistics", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

    # frame to hold the stat cards
    cards = tk.Frame(content, bg="white")
    cards.pack(pady=20)

    # ---- total playtime ----
    playtime_results = database.get_total_playtime(player_id)
    if playtime_results:
        total_hours = playtime_results[0][1]
    else:
        total_hours = 0

    # ---- library size ----
    library = database.get_player_library(player_id)
    library_count = len(library)

    # ---- wishlist size ----
    wishlist = database.get_wishlist(player_id)
    wishlist_count = len(wishlist)

    # ---- achievement count (across all games) ----
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM Achievement WHERE player_id = ? AND earned = 1",
        (player_id,)
    )
    earned_count = cursor.fetchone()[0]
    conn.close()

    # render four cards in a row
    stat_cards = [
        ("Total Playtime", f"{total_hours} hrs"),
        ("Games Owned",    str(library_count)),
        ("Wishlisted",     str(wishlist_count)),
        ("Achievements",   str(earned_count)),
    ]
    for i, (label, value) in enumerate(stat_cards):
        card = tk.Frame(cards, bg="#ecf0f1", relief="ridge", borderwidth=2,
                        width=160, height=100)
        card.grid(row=0, column=i, padx=10, pady=10)
        card.pack_propagate(False)
        tk.Label(card, text=value, bg="#ecf0f1",
                 font=("Arial", 20, "bold")).pack(pady=(15, 5))
        tk.Label(card, text=label, bg="#ecf0f1",
                 font=("Arial", 10)).pack()

    # ---- per-game playtime breakdown ----
    tk.Label(content, text="Playtime by Game", bg="white",
             font=("Arial", 14, "bold")).pack(pady=(20, 5))

    tree = ttk.Treeview(content, columns=("title", "hours"), show="headings", height=10)
    tree.heading("title", text="Game")
    tree.heading("hours", text="Hours Played")
    tree.column("title", width=300)
    tree.column("hours", width=120)
    tree.pack(padx=20, pady=5, fill="both", expand=True)

    for title, dev, playtime in library:
        tree.insert("", "end", values=(title, playtime))

    status.config(text="Stats loaded")


def show_library(content, status, player):
    # clears content frame. has the title and button row at the top, treeview table below, then we fill the table from the db
    clear_frame(content)
    player_id = player[0]

    tk.Label(content, text="My Library", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

    # button row across the top
    button_row = tk.Frame(content, bg="white")
    button_row.pack(pady=5)
    tk.Button(button_row, text="Add Game",
              command=lambda: open_add_game(player, content, status)).pack(side="left", padx=3)
    tk.Button(button_row, text="Edit Selected",
              command=lambda: edit_selected(tree, player, content, status)).pack(side="left", padx=3)
    tk.Button(button_row, text="Delete Selected",
              command=lambda: delete_selected(tree, player, content, status)).pack(side="left", padx=3)
    tk.Button(button_row, text="Set Digital",
              command=lambda: open_set_digital(tree, status)).pack(side="left", padx=3)
    tk.Button(button_row, text="Set Physical",
              command=lambda: open_set_physical(tree, status)).pack(side="left", padx=3)

    # the table itself
    columns = ("game_id", "title", "developer", "playtime")
    tree = ttk.Treeview(content, columns=columns, show="headings", height=15)
    tree.heading("game_id", text="ID")
    tree.heading("title", text="Title")
    tree.heading("developer", text="Developer")
    tree.heading("playtime", text="Playtime (hrs)")
    tree.column("game_id", width=50)
    tree.column("title", width=250)
    tree.column("developer", width=200)
    tree.column("playtime", width=120)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    # we need game_id in the table to know which game is selected,
    # but we don't really want the user staring at it so we hide it
    tree.column("game_id", width=0, stretch=False)
    tree["displaycolumns"] = ("title", "developer", "playtime")

    # fill the table from the database
    library = database.get_player_library(player_id)
    # get_player_library returns (title, developer, playtime) — no game_id.
    # We'll need the game_id for edit/delete, so let's grab it ourselves:
    refresh_library_table(tree, player_id)

    status.config(text=f"Library loaded ({len(library)} games)")

def refresh_library_table(tree, player_id):
    # clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    # query directly so we get game_id alongside the display fields
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Game.game_id, Game.title, Game.developer, Owns.playtime
        FROM Game
        JOIN Owns ON Game.game_id = Owns.game_id
        WHERE Owns.player_id = ?
    """, (player_id,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def get_selected_game_id(tree, status):
    """Returns the game_id of the selected row, or None with a status message."""
    selection = tree.selection()
    if not selection:
        status.config(text="Select a game first")
        return None
    return tree.item(selection[0])["values"][0]  # game_id is column 0


def delete_selected(tree, player, content, status):
    game_id = get_selected_game_id(tree, status)
    if game_id is None:
        return
    if not messagebox.askyesno("Confirm", "Delete this game from the catalog?"):
        return
    try:
        database.delete_game(game_id)
        status.config(text="Game deleted")
        show_library(content, status, player)  # refresh the whole screen
    except sqlite3.IntegrityError:
        status.config(text="Cannot delete — other records depend on it")


def edit_selected(tree, player, content, status):
    game_id = get_selected_game_id(tree, status)
    if game_id is None:
        return
    open_edit_game(game_id, player, content, status)

def open_add_game(player, content, status):
    win = tk.Toplevel(root)
    win.title("Add Game")
    win.geometry("350x300")

    fields = ["Title", "Release Date (YYYY-MM-DD)", "Rating (0-10)", "Platform", "Developer"]
    entries = {}
    for i, label in enumerate(fields):
        tk.Label(win, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        e = tk.Entry(win, width=25)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[label] = e

    def submit():
        try:
            rating = int(entries["Rating (0-10)"].get() or 0)
        except ValueError:
            rating = 0
        try:
            new_id = database.add_game(
                entries["Title"].get(),
                entries["Release Date (YYYY-MM-DD)"].get(),
                rating,
                entries["Platform"].get(),
                entries["Developer"].get(),
            )
            # also add it to the player's library
            try:
                database.add_to_library(player[0], new_id)
            except sqlite3.IntegrityError:
                pass
            status.config(text="Game added")
            win.destroy()
            show_library(content, status, player)
        except sqlite3.IntegrityError:
            status.config(text="A game with that title already exists")
            win.destroy()

    tk.Button(win, text="Add", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=15)



def open_set_digital(tree, status):
    selection = tree.selection()
    if not selection:
        status.config(text="Select a game first")
        return
    game_id = tree.item(selection[0])["values"][0]

    win = tk.Toplevel(root)
    win.title("Set Digital")
    tk.Label(win, text="File size:").grid(row=0, column=0, padx=5, pady=5)
    size_entry = tk.Entry(win); size_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(win, text="Store link:").grid(row=1, column=0, padx=5, pady=5)
    link_entry = tk.Entry(win); link_entry.grid(row=1, column=1, padx=5, pady=5)

    def submit():
        try:
            size = int(size_entry.get())
        except ValueError:
            status.config(text="Invalid file size"); return
        database.set_digital(game_id, size, link_entry.get())
        status.config(text="Set as digital")
        win.destroy()
    tk.Button(win, text="Save", command=submit).grid(row=2, column=0, columnspan=2, pady=10)


def open_set_physical(tree, status):
    selection = tree.selection()
    if not selection:
        status.config(text="Select a game first")
        return
    game_id = tree.item(selection[0])["values"][0]

    win = tk.Toplevel(root)
    win.title("Set Physical")
    tk.Label(win, text="Condition:").grid(row=0, column=0, padx=5, pady=5)
    cond_entry = tk.Entry(win); cond_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(win, text="Shelf location:").grid(row=1, column=0, padx=5, pady=5)
    shelf_entry = tk.Entry(win); shelf_entry.grid(row=1, column=1, padx=5, pady=5)

    def submit():
        database.set_physical(game_id, cond_entry.get(), shelf_entry.get())
        status.config(text="Set as physical")
        win.destroy()
    tk.Button(win, text="Save", command=submit).grid(row=2, column=0, columnspan=2, pady=10)


def show_wishlist(content, status, player):
    clear_frame(content)
    player_id = player[0]

    tk.Label(content, text="My Wishlist", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

    button_row = tk.Frame(content, bg="white")
    button_row.pack(pady=5)
    tk.Button(button_row, text="Add to Wishlist",
              command=lambda: open_add_to_wishlist(player, content, status)).pack(side="left", padx=3)
    tk.Button(button_row, text="Remove Selected",
              command=lambda: remove_from_wishlist_selected(tree, player, content, status)).pack(side="left", padx=3)

    columns = ("game_id", "title", "release_date")
    tree = ttk.Treeview(content, columns=columns, show="headings", height=15)
    tree.heading("title", text="Title")
    tree.heading("release_date", text="Release Date")
    tree.column("game_id", width=0, stretch=False)
    tree.column("title", width=300)
    tree.column("release_date", width=150)
    tree["displaycolumns"] = ("title", "release_date")
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    # populate — we need game_id again, so query directly
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Game.game_id, Game.title, Game.release_date
        FROM Game JOIN Wishlists ON Game.game_id = Wishlists.game_id
        WHERE Wishlists.player_id = ?
    """, (player_id,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    status.config(text="Wishlist loaded")


def open_add_to_wishlist(player, content, status):
    win = tk.Toplevel(root)
    win.title("Add to Wishlist")
    tk.Label(win, text="Game title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(win, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    def submit():
        matches = database.get_games_by_title(title_entry.get())
        if not matches:
            status.config(text="No game with that title")
            win.destroy()
            return
        if len(matches) > 1:
            status.config(text="Multiple matches — add disambiguation later")
            win.destroy()
            return
        try:
            database.add_to_wishlist(player[0], matches[0][0])
            status.config(text="Added to wishlist")
        except sqlite3.IntegrityError:
            status.config(text="Already on wishlist")
        win.destroy()
        show_wishlist(content, status, player)

    tk.Button(win, text="Add", command=submit).grid(row=1, column=0, columnspan=2, pady=10)


def remove_from_wishlist_selected(tree, player, content, status):
    selection = tree.selection()
    if not selection:
        status.config(text="Select a game first")
        return
    game_id = tree.item(selection[0])["values"][0]
    database.remove_from_wishlist(player[0], game_id)
    status.config(text="Removed from wishlist")
    show_wishlist(content, status, player)


def show_search(content, status, player):
    clear_frame(content)

    tk.Label(content, text="Search Games", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

    # search bar row
    bar = tk.Frame(content, bg="white")
    bar.pack(pady=5)
    tk.Label(bar, text="Search by:", bg="white").pack(side="left", padx=5)
    mode_var = tk.StringVar(value="title")
    ttk.Combobox(bar, textvariable=mode_var, values=["title", "genre", "tag"],
                 state="readonly", width=10).pack(side="left", padx=5)
    query_entry = tk.Entry(bar, width=30)
    query_entry.pack(side="left", padx=5)

    # results table
    tree = ttk.Treeview(content, columns=("title", "developer"), show="headings", height=15)
    tree.heading("title", text="Title")
    tree.heading("developer", text="Developer")
    tree.column("title", width=350)
    tree.column("developer", width=250)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    def do_search():
        for row in tree.get_children():
            tree.delete(row)
        query = query_entry.get()
        mode = mode_var.get()
        if mode == "title":
            results = database.search_by_title(query)
            # search_by_title returns 5-tuples; we only want title + developer
            for r in results:
                tree.insert("", "end", values=(r[0], r[4]))
        elif mode == "genre":
            for r in database.get_games_by_genre(query):
                tree.insert("", "end", values=r)
        elif mode == "tag":
            for r in database.get_games_by_tag(query):
                tree.insert("", "end", values=r)
        status.config(text=f"Found {len(tree.get_children())} games")

    tk.Button(bar, text="Search", command=do_search).pack(side="left", padx=5)
    # let Enter key trigger search too
    query_entry.bind("<Return>", lambda event: do_search())

def show_achievements(content, status, player):
    clear_frame(content)
    player_id = player[0]

    tk.Label(content, text="Achievements", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

    bar = tk.Frame(content, bg="white")
    bar.pack(pady=5)
    tk.Label(bar, text="Game title:", bg="white").pack(side="left", padx=5)
    title_entry = tk.Entry(bar, width=25)
    title_entry.pack(side="left", padx=5)

    tree = ttk.Treeview(content, columns=("name",), show="headings", height=15)
    tree.heading("name", text="Achievement")
    tree.column("name", width=400)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    # store the resolved game_id so the "Add" button knows what we last looked up
    state = {"game_id": None}

    def load_achievements():
        for row in tree.get_children():
            tree.delete(row)
        matches = database.get_games_by_title(title_entry.get())
        if not matches:
            status.config(text="No game with that title")
            state["game_id"] = None
            return
        state["game_id"] = matches[0][0]
        for (name,) in database.get_achievements(player_id, state["game_id"]):
            tree.insert("", "end", values=(name,))
        status.config(text=f"Loaded achievements for {matches[0][1]}")

    def open_add_achievement():
        if state["game_id"] is None:
            status.config(text="Look up a game first")
            return
        win = tk.Toplevel(root)
        win.title("Add Achievement")
        tk.Label(win, text="Achievement name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(win, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        def submit():
            try:
                database.add_achievement(player_id, state["game_id"], name_entry.get())
                status.config(text="Achievement added")
            except sqlite3.IntegrityError:
                status.config(text="Couldn't add achievement")
            win.destroy()
            load_achievements()

        tk.Button(win, text="Add", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    tk.Button(bar, text="Load", command=load_achievements).pack(side="left", padx=5)
    tk.Button(bar, text="Add Achievement", command=open_add_achievement).pack(side="left", padx=5)


def show_tags_genres(content, status, player):
    clear_frame(content)

    tk.Label(content, text="Tags & Genres", bg="white", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(content, text="Assign a tag or genre to a game", bg="white", fg="gray").pack()

    form = tk.Frame(content, bg="white")
    form.pack(pady=20)

    tk.Label(form, text="Game title:", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    title_entry = tk.Entry(form, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Tag name:", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tag_entry = tk.Entry(form, width=30)
    tag_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(form, text="Assign Tag",
              command=lambda: assign_tag_action(title_entry.get(), tag_entry.get(), status)
              ).grid(row=1, column=2, padx=5)

    tk.Label(form, text="Genre name:", bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    genre_entry = tk.Entry(form, width=30)
    genre_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(form, text="Assign Genre",
              command=lambda: assign_genre_action(title_entry.get(), genre_entry.get(), status)
              ).grid(row=2, column=2, padx=5)


def assign_tag_action(title, tag_name, status):
    matches = database.get_games_by_title(title)
    if not matches:
        status.config(text="No game with that title"); return
    try:
        database.assign_tag(matches[0][0], tag_name)
        status.config(text=f"Tag '{tag_name}' assigned")
    except sqlite3.IntegrityError:
        status.config(text="Couldn't assign tag")


def assign_genre_action(title, genre_name, status):
    matches = database.get_games_by_title(title)
    if not matches:
        status.config(text="No game with that title"); return
    try:
        database.assign_genre(matches[0][0], genre_name)
        status.config(text=f"Genre '{genre_name}' assigned")
    except sqlite3.IntegrityError:
        status.config(text="Couldn't assign genre")


show_login()

root.mainloop() #this is the loop that looks for inputs
