# -*- coding: utf-8 -*-

import datetime
from util import insert_privileges

class NoSuchUserError(Exception): pass
class NoSuchCaseError(Exception): pass

def set_privileges(dbconn, user, investigation, privileges):
    cur = dbconn.cursor()

    # sprawdzamy, czy istnieje użytkownik

    cur.execute("SELECT NULL FROM uzytkownicy WHERE Policjant=%s", (user,))
    if(cur.rowcount == 0):
        raise NoSuchUserError

    # sprawdzamy, czy istnieje sprawa

    cur.execute("SELECT NULL FROM sprawy WHERE Sprawa=%s", (investigation,))
    if(cur.rowcount == 0):
        raise NoSuchCaseError

    # sprawdzamy, czy użytkownik ma uprawnienia do sprawy
    cur.execute("SELECT NULL FROM uprawnienia WHERE Sprawa=%s AND Policjant=%s", (investigation, user))
    
    # nie ma:
    if cur.rowcount == 0:
        if privileges == None:
            return
        else:
            insert_privileges(dbconn, (investigation, user, privileges))

    #  ma:
    elif cur.rowcount == 1:                                 
        if privileges == None:
            cur.execute("DELETE FROM uprawnienia WHERE Sprawa=%s AND Policjant=%s", (investigation, user))
        else:
            cur.execute("UPDATE uprawnienia SET Uprawnienia=%s WHERE Sprawa=%s AND Policjant=%s", (privileges, investigation, user))

class CaseExists(Exception): pass
                              
def create_case(dbconn, owner, case):
    cur = dbconn.cursor()
    #sprawdzamy czy sprawa nie istnieje
    cur.execute("SELECT NULL FROM sprawy WHERE sprawa=%s", (case,))
    if(cur.rowcount != 0):
        raise CaseExists
    #jesli nie to tworzymy
    now = datetime.datetime.now()
    cur.execute("INSERT INTO sprawy (sprawa, policjant, data_otwarcia) VALUES (%s, %s, %s)",
                (case,owner,datetime.date(now.year,now.month,now.day)))

def close_case(dbconn, owner, case):
    cur = dbconn.cursor()
    #sprawdzamy czy sprawa juz istnieje
    cur.execute("SELECT * FROM sprawy WHERE sprawa=%s AND policjant=%s", (case,owner))
    if(cur.rowcount != 1):
        raise NoSuchCaseError
    #jesli tak to ja zamykamy
    now = datetime.datetime.now()
    cur.execute("UPDATE sprawy SET data_zamkniecia=%s WHERE sprawa=%s AND policjant=%s",
                (datetime.date(now.year,now.month,now.day),case,owner))

def delete_case(dbconn, owner, case):
    cur = dbconn.cursor()
    cur.execute("DELETE FROM sprawy WHERE sprawa=%s AND policjant=%s",(case,owner))
