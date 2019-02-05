import MySQLdb

class MySQLDriver:
    def __init__(self, src):
        self.db = MySQLdb.connect(**src)

        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def get(self, query):
            try:
                self.cursor.execute(query['op'], query['params'])
            except:
                return None

            return self.cursor.fetchall()

    def post(self, query):
        try:
            self.cursor.execute(query['op'], query['params'])
            self.db.commit()
        except:
            return None

        return self.cursor.lastrowid

