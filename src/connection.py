import sqlite3

class Db():
    def __init__(self):
        try:
            self.conn = sqlite3.connect("db/miniproyecto.db")
        except sqlite3.Error:
            print(sqlite3.Error)

    def createDataBase(self):
        cursorObj = self.conn.cursor()
        cursorObj.execute(f"Create table Region(id integer not null primary key AUTOINCREMENT, Region varchar(50) not null, City varchar(50) not null, Language varchar(100) not null, Time Float )")

    def checkTableName(self, table_name):

        cursorObj = self.conn.cursor()
        #cursorObj.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        cursorObj.execute(f"SELECT * FROM Region")


        return cursorObj.fetchall()

    def saveDataframe(self,df, table_name):
        
        df.to_sql(table_name, self.conn, if_exists='append', index=False)
        #print(self.checkTableName(table_name))
    
    def closeConnection(self):
        self.conn.close()