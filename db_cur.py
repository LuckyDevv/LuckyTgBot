import sqlite3


#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
class DBcur:
    def __init__(self, file):
        self.db = sqlite3.connect(file, check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, balance REAL);")
        self.db.execute("CREATE TABLE IF NOT EXISTS gardens (id INTEGER PRIMARY KEY, lvl INTEGER, last_cost REAL);")
        self.db.execute("CREATE TABLE IF NOT EXISTS offices (id INTEGER PRIMARY KEY, lvl INTEGER, last_cost REAL);")
        self.cur = self.db.cursor()

    def get_office(self, cid):
        try:
            idd, lvl, last_cost = self.cur.execute(f"SELECT * FROM offices WHERE id = {cid};").fetchone()
            if lvl != 0:
                earn = 0
                i = 0
                while i < lvl:
                    earn += 1
                    i += 1
                return earn-1
            else:
                return 0
        except:
            return 0

    def get_office_last_cost(self, cid):
        try:
            idd, lvl, last_cost = self.cur.execute(f"SELECT * FROM offices WHERE id = {cid};").fetchone()
            return last_cost
        except:
            return 0

    def update_office(self, cid):
        office = self.get_office(cid) + 1
        self.cur.execute(f"UPDATE offices SET lvl = {office} WHERE id={int(cid)};")
        self.cur.connection.commit()

    def update_office_last_cost(self, cid, cost):
        self.cur.execute(f"UPDATE offices SET last_cost = {cost} WHERE id={int(cid)};")
        self.cur.connection.commit()

    def get_garden(self, cid):
        try:
            idd, lvl, last_cost = self.cur.execute(f"SELECT * FROM gardens WHERE id={cid};").fetchone()
            lvl = (lvl - 0.001) * 1000
            if lvl != 0:
                boost = 0.001
                i = 0
                while i < lvl:
                    boost += 0.001
                    i += 1
                return boost
            else:
                return 0.001
        except:
            return 0.001

    def get_garden_trees(self, cid):
        try:
            idd, lvl, last_cost = self.cur.execute(f"SELECT * FROM gardens WHERE id={cid};").fetchone()
            return lvl
        except:
            return 0

    def get_garden_last_cost(self, cid):
        try:
            idd, lvl, last_cost = self.cur.execute(f"SELECT * FROM gardens WHERE id={cid};").fetchone()
            return last_cost
        except:
            return 0

    def update_garden(self, cid):
        garden = self.get_garden(cid) + 0.001
        self.cur.execute(f"UPDATE gardens SET lvl = {garden} WHERE id={int(cid)};")
        self.cur.connection.commit()

    def update_garden_last_cost(self, cid, cost):
        self.cur.execute(f"UPDATE gardens SET last_cost = {cost} WHERE id={int(cid)};")
        self.cur.connection.commit()

    def get_top(self):
        players = self.cur.execute("SELECT * FROM users").fetchall()
        players = sorted(players, reverse=True, key=lambda player_: player_[2])
        top = ''
        i = 0
        for player in players:
            if i < 10:
                top += f'<b>№{i + 1}. {str(player[1])}</b>: {str(round(float(player[2]), 2))} LC\n'
            i += 1
        return top

    def set_balance(self, cid, user_name, new_balance):
        try:
            if self.get_balance(cid) == -2:
                self.cur.execute(f"INSERT INTO users (id, user_name, balance) VALUES ({int(cid)}, '{user_name}' 0);")
                self.cur.connection.commit()
            else:
                self.cur.execute(f"UPDATE users SET balance = {new_balance} WHERE id={int(cid)};")
                self.cur.connection.commit()
            return True
        except:
            return False

    def get_balance(self, cid):
        try:
            fetch = self.cur.execute(f"SELECT * FROM users WHERE id={int(cid)}").fetchone()
            if fetch is None:
                return -2
            else:
                return round(float(fetch[2]), 2)
        except:
            return -2

    def create_player(self, cid, full_name):
        try:
            self.cur.execute(f"INSERT INTO users (id, user_name, balance) VALUES ({int(cid)}, '{full_name}', 0);")
            self.cur.execute(f"INSERT INTO offices (id, lvl, last_cost) VALUES ({int(cid)}, 0, 0);")
            self.cur.execute(f"INSERT INTO gardens (id, lvl, last_cost) VALUES ({int(cid)}, 0, 0);")
            self.cur.connection.commit()
            return True
        except:
            return False

    def get_name(self, cid):
        try:
            fetch = self.cur.execute(f"SELECT * FROM users WHERE id={int(cid)}").fetchone()
            return fetch[1]
        except:
            return False
