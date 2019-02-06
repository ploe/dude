import MySQLdb

class MySQLDriver:
    def __init__(self, src):
        self.db = MySQLdb.connect(**src)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def read(self, query):
            try:
                self.cursor.execute(query['op'], query['params'])
            except Exception as e:
                return None

            return self.cursor.fetchall()

    def create(self, query):
        return self.write(query)

    def update(self, query):
        return self.write(query)

    def write(self, query):
        try:
            self.cursor.execute(query['op'], query['params'])
            self.db.commit()
        except:
            return None

        return self.cursor.lastrowid

    def delete(self, query):
        try:
            self.cursor.execute(query['op'], query['params'])
            self.db.commit()
        except:
            return None

        return self.cursor.rowcount
