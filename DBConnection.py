import sqlite3


class DBConnect:

    def __init__(self, dbname):
        self.__dbname = dbname
        self.__con = sqlite3.connect('{}'.format(self.__dbname))

    def to_table(self, table, raw_urlset):
        urlset = list(raw_urlset.items())
        if not any(self.__con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table))):
            self.__con.execute('''CREATE TABLE '{}' (site text NOT NULL, url text NOT NULL, nex_urls text)'''.format(table))
        for url in urlset:
            self.__con.execute('''INSERT INTO '{}' VALUES (?, ?, ?)'''.format(table), (str(urlset[0][0]), str(url[0]), str(url[1])))

    def commit(self):
        self.__con.commit()

    def __del__(self):
        self.__con.close()
