# -*- coding: utf-8 -*-

import psycopg2
import unittest
import core

class InvestigationEditingTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect("port=5432 host=metodyki.dyndns.org dbname=test user=pguser password='tylkosystemlinux'")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE uprawnienia ( id serial PRIMARY KEY, Sprawa varchar(255), Policjant varchar(255), Uprawnienia varchar(255) );" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P100','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P101','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P102','odczyt/zapis');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P103','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P104','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S100','P105','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S101','P100','odczyt');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S101','P101','odczyt/zapis');" + \
        "INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES ('S102','P100','odczyt/zapis')")

    def tearDown(self):
        self.cur.execute("DROP TABLE uprawnienia")
        self.cur.close()
        self.conn.close()

    # opcjonalnie można potem sprawdzać całą tabelę (albo przynajmniej czy liczba rekordów się zgadza)

    # brak sprawy
    def test_NoSuchCase(self):
        with self.assertRaises(core.NoSuchCaseError):
            core.set_privileges('S105','P100','odczyt')

    # brak użytkownika
    def test_NoSuchUser(self):
        with self.assertRaises(core.NoSuchUserError):
            core.set_privileges('S100', 'P106', 'odczyt/zapis')

    # usunięcie uprawnień
    def test_TakeAwayPrivileges(self):
        core.set_privileges('S100', 'P102', None)
        self.cur.execute("SELECT NULL FROM uprawnienia WHERE Sprawa='S100' AND Policjant='P102'")
        self.assertEqual(self.cur.rowcount, 0)

    # zmiana uprawnień
    def test_ChangePrivileges(self):
        core.set_privileges('S101', 'P100', 'odczyt/zapis')
        self.cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P100'")
        self.assertEqual(self.cur.rowcount, 1)
        (privileges,) = self.cur.fetchone()
        self.assertEqual(privileges, 'odczyt/zapis')

    # dodanie uprawnień do sprawy nowemu użytkownikowi
    def test_GivePrivileges(self):
        core.set_privileges('S101', 'P105', 'odczyt')
        self.cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P105'")
        self.assertEqual(self.cur.rowcount, 1)
        (privileges,) = self.cur.fetchone()
        self.assertEqual(privileges, 'odczyt')

suite = unittest.TestLoader().loadTestsFromTestCase(InvestigationEditingTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
