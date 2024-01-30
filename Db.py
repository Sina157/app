import sqlite3

DbName = "DbApp.sqlite3"

def CreateTables(DataBaseName=DbName):
        conn = sqlite3.connect(DataBaseName)
        query = conn.cursor()
        query.execute('''
        CREATE TABLE IF NOT EXISTS Users
        ([ID]  INTEGER PRIMARY KEY,
        [visited]	INTEGER,
        [submited]	INTEGER,
        [IP]    TEXT,
        [Scode]    TEXT
        )
        ''')
    
    
def AddOrUpdate(IP , Scode , DataBaseName=DbName):
            conn = sqlite3.connect(DataBaseName)
            query = conn.cursor()
            FoundUserID = query.execute(f'''
                SELECT ID FROM Users WHERE IP = "{IP}" OR Scode = "{Scode}";
                ''').fetchone()
            if (FoundUserID != None):
                query.execute(f'''
                    UPDATE Users
                    SET submited = submited + 1
                    WHERE ID = "{FoundUserID[0]}";
                ''')
            else:
                query.execute(f'''
                        INSERT INTO Users (IP , Scode , visited , submited)
                                VALUES
                                ("{IP}", "{Scode}" ,0, 1)
                        ''')
            conn.commit()

def onVisitEvent(IP, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
                    UPDATE Users
                    SET visited = visited + 1
                    WHERE IP = "{IP}";
                ''')
    conn.commit()

def GetUserByIP(IP, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE IP = "{IP}";
                ''').fetchone()
    return User

CreateTables()
