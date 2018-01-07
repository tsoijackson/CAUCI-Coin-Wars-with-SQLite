
import sqlite3
from collections import namedtuple

DB_FILE = "coinwars.db"
Player = namedtuple('Player', 'name points coins dollars')

def create_connection(db_file):
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_table(conn: sqlite3):
    command = ('CREATE TABLE IF NOT EXISTS coinwars_db('
               'name TEXT PRIMARY KEY,'
               'points REAL DEFAULT 0,'
               'coins REAL DEFAULT 0,'
               'dollars REAL DEFAULT 0)')
    conn.cursor().execute(command)

def select_player_by_points(conn: sqlite3) -> [Player]:
    result = []
    command = ('Select * FROM coinwars_db ORDER BY points, coins DESC;')
    for i in conn.cursor().execute(command):
        result.append(Player(i[0], "{:.2f}".format(float(i[1])), "{:.2f}".format(i[2]), "{:.2f}".format(i[3])))
    return result

def name_exists(conn: sqlite3, name: str) -> bool:
    player_list = select_player_by_points(conn)
    for player in player_list:
        if name == player.name:
            return True
    return False

def update_player(conn: sqlite3):
    player_name = input("Enter Player Name: ").lower()
    if not name_exists(conn, player_name):
        print("Player Name does not Exist")
        print()
        return

    coins = input("Enter Coins Amt: ")
    try:
        coins = float(coins)
    except:
        print("Incorrect Input. Please input a Number")
        print()
        return

    dollars =  input("Enter Dollars Amt: ")
    try:
        dollars = float(dollars)
    except:
        print("Incorrect Input. Please input a Number")
        print()
        return

    points = coins - dollars

    command = """
        UPDATE coinwars_db
        SET points = {}, coins = {}, dollars = {}
        WHERE name = '{}';
    """.format(points, coins, dollars, player_name)

    conn.cursor().execute(command)
    conn.commit()

    print("Player Stats have been Updated!")

def update_all_players(conn: sqlite3):
    player_list = select_player_by_points(conn)
    try:
        for player in player_list:
            print("Current Player: " + str(player))

            coins = input("Enter Coins Amt: ")
            try:
                coins = float(coins)
            except:
                print("Incorrect Input. Please input a Number")
                print()
                return

            dollars = input("Enter Dollars Amt: ")
            try:
                dollars = float(dollars)
            except:
                print("Incorrect Input. Please input a Number")
                print()
                return

            points = coins - dollars

            command = """
                UPDATE coinwars_db
                SET points = {}, coins = {}, dollars = {}
                WHERE name = '{}';
            """.format(points, coins, dollars, player.name)

            conn.cursor().execute(command)
            conn.commit()
    except:
        print("Something went Wrong!:( Possibly wrong input. Operation unsuccessful and returning to Menu...")
        return

def add_new_player(conn: sqlite3):
    player_name = input("Enter Player Name to Add: ").lower()

    if name_exists(conn, player_name):
        print("Player name already in Database. Returning to Menu...")
        print()
        return

    print("Adding New Player...")
    command = ('INSERT INTO coinwars_db (name) VALUES (\'' + player_name + '\');')
    conn.cursor().execute(command)
    conn.commit()
    print("New Player Sucessfully Added!")
    print()

def remove_a_player(conn: sqlite3):
    player_name = input("Enter Player Name to Remove: ").lower()

    if not name_exists(conn, player_name):
        print("Player Name does not Exist. Cannot remove Name. Returning to Menu...")
        print()
        return

    command = ('DELETE FROM coinwars_db WHERE name = \'' + player_name + '\'')

    conn.cursor().execute(command)
    conn.commit()

def clear_all_players(conn: sqlite3):
    print("Clearing all Players ...")
    command = ('DROP TABLE coinwars_db')
    conn.cursor().execute(command) #Drop current table
    create_table(conn) #Create new table
    print("All Players Cleared!")
    print()

############### MENU / INTERFACE ###############

def print_welcome():
    print("Welcome to CAUCI Coin Wars!")
    print()
    print("Coin Wars is a yearly fundraiser that CAUCI does every winter quarter.")
    print("The goal of the fundraiser is to collect unwanted change and the")
    print("player with most change wins, but the twist is that people can donate whole")
    print("dollar bills to players to bring their score down to prevent them from winning!")
    print()

    print("Rules:")
    print("  1. Player placement is dependent on points")
    print("  2. Points = Coins - Dollars")
    print("  3. When updating coin/dollar amt, please format as XX.XX")
    print("       Ex) $5 in coins/dollars means inputting 5 or 5.00")
    print("       Ex) $3.81 in coins/dollars means inputting 3.81")
    print()

def print_table(conn: sqlite3):
    table = ""
    border = " +------------+---------+---------+---------+" + '\n'
    table += border
    table += " |{:^12}|{:^9}|{:^9}|{:^9}|".format("Name", "Points", "Coins", "Dollars") + '\n'
    table += border

    player_list = select_player_by_points(conn)
    for player in player_list:
        table += " |{:^12}|{:^9}|{:^9}|{:^9}|".format(player.name, player.points, player.coins, player.dollars) + '\n'

    table += border
    print(table)
    print()

def print_stats(conn: sqlite3):
    amt_raised = 0
    player_list = select_player_by_points(conn)
    for player in player_list:
        amt_raised += float(player.coins) + float(player.dollars)
    print("{:19}: ${:.2f}".format("Current Amt Raised", amt_raised))
    print()

def print_menu():
    print("Coin Wars Menu: ")
    print("  A. Update a Player's Coins & Dollars")
    print("  B. Update all Players' Coins & Dollars")
    print("  C. Add New Player")
    print("  D. Remove a Player")
    print("  E. Clear all Players")
    print("  Q. Quit")
    print()

def main_interface():
    conn = create_connection(DB_FILE)
    create_table(conn)

    print_welcome()
    response = None #initialize response

    while response != "Q":
        print_stats(conn)
        print_table(conn)
        print_menu()
        response = input("Menu Choice: ").upper()

        if response == "A":
            update_player(conn)
        elif response == "B":
            update_all_players(conn)
        elif response == "C":
            add_new_player(conn)
        elif response == "D":
            remove_a_player(conn)
        elif response == "E":
            clear_all_players(conn)
        elif response == "Q":
            print("Exiting Menu ...")
            pass
        else:
            print("Please Enter a Letter Choice on the Menu")
            print()
            continue

if __name__ == '__main__':
    main_interface()