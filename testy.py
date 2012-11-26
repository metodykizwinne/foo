#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# CREATE TABLE uprawnienia ( id serial PRIMARY KEY, Sprawa varchar(255), Policjant varchar(255), Uprawnienia varchar(255) )

import unittest
import psycopg2
from functools import partial

import core
from util import insert_privileges, TESTDBNAME, TESTUSER, HOST, TESTPASSWORD

class InvestigationEditingTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s password='%s'" % (TESTDBNAME, TESTUSER, HOST, TESTPASSWORD))
        self.cur = self.conn.cursor()
        test_privileges = [ ('S100','P100','odczyt'),
                            ('S100','P101','odczyt'),
                            ('S100','P102','odczyt/zapis'),
                            ('S100','P103','odczyt'),
                            ('S100','P104','odczyt'),
                            ('S100','P105','odczyt'),
                            ('S101','P100','odczyt'),
                            ('S101','P101','odczyt/zapis'),
                            ('S102','P100','odczyt/zapis') ]
        map(partial(insert_privileges, self.conn), test_privileges)

    def tearDown(self):
        self.cur.execute("DELETE FROM uprawnienia")
        self.cur.close()
        self.conn.close()

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

class CaseCreationTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s password='%s'" % (TESTDBNAME, TESTUSER, HOST, TESTPASSWORD))
        self.cur = self.conn.cursor()
        # wsadz sprawe S100 i policjanta P100
        pass

    # sprawa już istnieje
    def test_CaseExists(self):
        with self.assertRaises(core.CaseExists):
            create_case(self.conn, 'P100', 'S100')
            
    # utworzenie pustej sprawy
    def test_NewCase(self):
        create_case(self.conn, 'P100', 'S666')
        self.cur.execute("SELECT * FROM sprawy WHERE Sprawa=S666")
        self.assertEqual(self.cur.rowcount, 1)
        (id, name, owner, creation_date, closure_date) = self.cur.fetchone()
        self.assertEqual(owner, 'P100')
        # coś tam dalej

    def tearDown(self):
        self.cur.execute("DELETE FROM uprawnienia")
        self.cur.close()
        self.conn.close()

# do wyboru
suite = unittest.TestLoader().loadTestsFromTestCase(InvestigationEditingTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(CaseCreationTestCase)
###########

unittest.TextTestRunner(verbosity=2).run(suite)
