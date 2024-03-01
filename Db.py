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
        query.execute('''
        CREATE TABLE IF NOT EXISTS NationalCodes
        ([ID]  INTEGER PRIMARY KEY,
        [NationalCode] TEXT,
        [Submitted] INTEGER
        )
                  ''')
    
    
def AddOrUpdateToUsers(IP , Scode  , NationalCode , DataBaseName=DbName):
            Scode = Scode.replace('"','') # sql injection
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
                                ("{IP}", "{Scode}" ,1, 1 , "{NationalCode}")
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

def GetUserByIP(IP, DataBaseName=DbName) -> dict:
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE IP = "{IP}";
                ''').fetchone()
    if User is None:
        return None
    User = dict(zip([column[0] for column in query.description], User))
    return User

def GetUserByScode(Scode, DataBaseName=DbName) -> dict:
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE Scode = "{Scode}";
                ''').fetchone()
    if User is None:
        return None
    User = dict(zip([column[0] for column in query.description], User))
    return User

def GetUsersByNationalCode(NationalCode, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    User = query.execute(f'''
                SELECT * FROM Users WHERE NationalCode = "{NationalCode}";
                ''').fetchone()
    if User is None:
        return None
    User = dict(zip([column[0] for column in query.description], User))
    return User
# ============================ NationalCodes ============================

def AddOrUpdateToNationalCode(NationalCode , DataBaseName=DbName):
            conn = sqlite3.connect(DataBaseName)
            query = conn.cursor()
            FoundNationalCodeID = query.execute(f'''
                SELECT ID FROM NationalCodes WHERE NationalCode = "{NationalCode}";
                ''').fetchone()
            if (FoundNationalCodeID != None):
                query.execute(f'''
                    UPDATE NationalCodes
                    SET Submitted = Submitted + 1
                    WHERE ID = {FoundNationalCodeID[0]};
                ''')
            else:
                query.execute(f'''
                        INSERT INTO NationalCodes (NationalCode , Submitted)
                                VALUES
                                ("{NationalCode}",1)
                        ''')
            conn.commit()

def GetNationalSubmitted(NationalCode, DataBaseName=DbName):
    conn = sqlite3.connect(DataBaseName)
    query = conn.cursor()
    Count = query.execute(f'''
                SELECT Submitted FROM NationalCodes WHERE NationalCode = "{NationalCode}";
                ''').fetchone()
    if Count == None:
        return '0'
    else:
        return str(Count[0])


CreateTables()

