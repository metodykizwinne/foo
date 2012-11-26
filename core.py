# -*- coding: utf-8 -*-

from util import insert_privileges

class NoSuchUserError(Exception): pass
class NoSuchCaseError(Exception): pass

def set_privileges(dbconn, user, investigation, privileges):
    cur = dbconn.cursor()

    # # sprawdzamy, czy istnieje użytkownik

    # cur.execute("SELECT NULL FROM uzytkownicy WHERE Policjant=%s", (user,))
    # if(cur.rowcount == 0):
    #     raise NoSuchUserError

    # # sprawdzamy, czy istnieje sprawa

    # cur.execute("SELECT NULL FROM sprawy WHERE Sprawa=%s", (investigation,))
    # if(cur.rowcount == 0):
    #     raise NoSuchCaseError

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
    pass
