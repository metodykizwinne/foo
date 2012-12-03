# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

import datetime

# CREATE TABLE uprawnienia ( id serial PRIMARY KEY, Sprawa varchar(255), Policjant varchar(255), Uprawnienia varchar(255) )

import unittest
import psycopg2
from functools import partial

import core
from util import *

# klasa abstrakcyjna dla testów korzystających z bazy danych
class DBTestCase(unittest.TestCase):
    def prepareDB(self):
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s password='%s'" % (TESTDBNAME, TESTUSER, HOST, TESTPASSWORD))
        self.cur = self.conn.cursor()
        map(partial(insert_privileges, self.conn), self.privileges)
        map(partial(insert_investigation, self.conn), self.cases)
        map(partial(insert_user, self.conn), self.users)

    def tearDown(self):
        self.cur.execute("DELETE FROM uprawnienia")
        self.cur.execute("DELETE FROM sprawy")
        self.cur.execute("DELETE FROM uzytkownicy")
        self.cur.close()
        self.conn.close()

class InvestigationEditingTestCase(DBTestCase):

    def setUp(self):
        self.privileges = [ ('S100','P100','odczyt'),
                            ('S100','P101','odczyt'),
                            ('S100','P102','odczyt/zapis'),
                            ('S100','P103','odczyt'),
                            ('S100','P104','odczyt'),
                            ('S100','P105','odczyt'),
                            ('S101','P100','odczyt'),
                            ('S101','P101','odczyt/zapis'),
                            ('S102','P100','odczyt/zapis') ]
        self.cases = [('S100', 'P666', '2001-01-01', None),
                      ('S101', 'P666', '2001-01-01', None),
                      ('S102', 'P666', '2001-01-01', None)]
        self.users = [('P100', 'AAA', 'BBB'),
                      ('P101', 'AAA', 'BBB'),
                      ('P102', 'AAA', 'BBB'),
                      ('P103', 'AAA', 'BBB'),
                      ('P104', 'AAA', 'BBB'),
                      ('P105', 'AAA', 'BBB'),
                      ('P666', 'AAA', 'BBB')]
        self.prepareDB()


    # opcjonalnie można potem sprawdzać całą tabelę (albo przynajmniej czy liczba rekordów się zgadza)

    # brak sprawy
    def test_NoSuchCase(self):
        with self.assertRaises(core.NoSuchCaseError):
            core.set_privileges(self.conn, 'P100', 'S105', 'odczyt')

    # brak użytkownika
    def test_NoSuchUser(self):
        with self.assertRaises(core.NoSuchUserError):
            core.set_privileges(self.conn, 'P106', 'S100', 'odczyt/zapis')

    # usunięcie uprawnień
    def test_TakeAwayPrivileges(self):
        core.set_privileges(self.conn, 'P102', 'S100', None)
        self.cur.execute("SELECT NULL FROM uprawnienia WHERE Sprawa='S100' AND Policjant='P102'")
        self.assertEqual(self.cur.rowcount, 0)

    # zmiana uprawnień
    def test_ChangePrivileges(self):
        core.set_privileges(self.conn, 'P100', 'S101', 'odczyt/zapis')
        self.cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P100'")
        self.assertEqual(self.cur.rowcount, 1)
        (privileges,) = self.cur.fetchone()
        self.assertEqual(privileges, 'odczyt/zapis')

    # dodanie uprawnień do sprawy nowemu użytkownikowi
    def test_GivePrivileges(self):
        core.set_privileges(self.conn, 'P105', 'S101', 'odczyt')
        self.cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P105'")
        self.assertEqual(self.cur.rowcount, 1)
        (privileges,) = self.cur.fetchone()
        self.assertEqual(privileges, 'odczyt')

class CaseCreationTestCase(DBTestCase):
    def setUp(self):
        self.privileges = []
        self.cases = [('S100', 'P666', '2001-01-01', None)]
        self.users = [('P100', 'AAA', 'BBB')]
        self.prepareDB()

    # sprawa już istnieje
    def test_CaseExists(self):
        with self.assertRaises(core.CaseExists):
            core.create_case(self.conn, 'P100', 'S100')
            
    # utworzenie pustej sprawy
    def test_NewCase(self):
        core.create_case(self.conn, 'P100', 'S666')
        self.cur.execute("SELECT * FROM sprawy WHERE Sprawa='S666'")
        self.assertEqual(self.cur.rowcount, 1)
        (id, name, owner, creation_date, closure_date) = self.cur.fetchone()
        self.assertEqual(owner, 'P100')
        now = datetime.datetime.now()
        self.assertEqual(creation_date, datetime.date(now.year, now.month, now.day))
        self.assertEqual(closure_date, None)

class CaseClosureTestCase(DBTestCase):
    def setUp(self):
        self.privileges = []
        self.cases = [('S100', 'P100', '2001-01-01', None)]
        self.users = [('P100', 'AAA', 'BBB')]
        self.prepareDB()

    # sprawa nie istnieje
    def test_NoSuchCase(self):
        with self.assertRaises(core.NoSuchCaseError):
            core.close_case(self.conn, 'P100', 'S101')

    def test_CaseClosure(self):
        core.close_case(self.conn, 'P100', 'S100')
        self.cur.execute("SELECT Data_zamkniecia FROM sprawy WHERE Sprawa=%s", ('S100',))
        (closure_date,) = self.cur.fetchone()
        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)
        self.assertEqual(closure_date, today)
        
        

# do wyboru
suite = unittest.TestLoader().loadTestsFromTestCase(InvestigationEditingTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(CaseCreationTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(CaseClosureTestCase)
###########

unittest.TextTestRunner(verbosity=2).run(suite)
