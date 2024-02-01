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
        [Scode]    TEXT,
        [NationalCode] TEXT
        )
        ''')
    
    
def AddOrUpdate(IP , Scode  , NationalCode , DataBaseName=DbName):
            conn = sqlite3.connect(DataBaseName)
            query = conn.cursor()
            FoundUserID = query.execute(f'''
                SELECT ID FROM Users WHERE IP = "{IP}" OR Scode = "{Scode}";
                ''').fetchone()
            if (FoundUserID != None):
                query.execute(f'''
                    UPDATE Users
                    SET submited = submited + 1,
                    NationalCode = "{NationalCode}"
                    WHERE ID = "{FoundUserID[0]}";
                ''')
            else:
                query.execute(f'''
                        INSERT INTO Users (IP , Scode , visited , submited ,NationalCode)
                                VALUES
                                ("{IP}", "{Scode}" ,0, 1 , "{NationalCode}")
                        ''')
            conn.commit()


def onVisitIp(IP, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
                    UPDATE Users
                    SET visited = visited + 1
                    WHERE IP = "{IP}";
                ''')
    conn.commit()

def onVisitScode(Scode, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    query.execute(f'''
                    UPDATE Users
                    SET visited = visited + 1
                    WHERE Scode = "{Scode}";
                ''')
    conn.commit()

def GetUserByIP(IP, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE IP = "{IP}";
                ''').fetchone()
    return User

def GetUserByScode(Scode, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE Scode = "{Scode}";
                ''').fetchone()
    return User

def GetUsersByNationalCode(NationalCode, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE NationalCode = "{NationalCode}";
                ''').fetchall()
    return User

CreateTables()

