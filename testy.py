# -*- coding: utf-8 -*-

import psycopg2
import unittest
import core

class InvestigationEditingTC(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect("port=5432 host=metodyki.dyndns.org dbname=test user=pguser password='tylkosystemlinux'")
        self.cur = conn.cursor()
        self.cur.execute("CREATE TABLE uprawnienia ( id serial PRIMARY KEY, Sprawa varchar(255), Policjant varchar(255), Uprawnienia varchar(255) );" + \
        "INSERT INTO uprawnienia VALUES ('S100','P100','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S100','P101','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S100','P102','odczyt/zapis');" + \
        "INSERT INTO uprawnienia VALUES ('S100','P103','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S100','P104','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S100','P105','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S101','P100','odczyt');" + \
        "INSERT INTO uprawnienia VALUES ('S101','P101','odczyt/zapis');" + \
        "INSERT INTO uprawnienia VALUES ('S102','P100','odczyt/zapis')")

    def tearDown(self):
        self.cur.execute("DROP TABLE uprawnienia")

# opcjonalnie można potem sprawdzać całą tabelę (albo przynajmniej czy liczba rekordów się zgadza)
        
class NoSuchCaseTC(InvestigationEditingTC):
    # brak sprawy
    def runTest(self):
        with self.assertRaises(NoSuchCaseError):
            core.set_privileges('S105','P100','odczyt')

class NoSuchUserTC(InvestigationEditingTC):
    # brak użytkownika
    def runTest(self):
        with self.assertRaises(NoSuchUserError):
            core.set_privileges('S100', 'P106', 'odczyt/zapis')

class TakeAwayPrivilegesTC(InvestigationEditingTC):            
    # usunięcie uprawnień
    def runTest(self):
        core.set_privileges('S100', 'P102', None)
        cur.execute("SELECT NULL FROM uprawnienia WHERE Sprawa='S100' AND Policjant='P102'")
        self.assertEqual(cur.rowcount, 0)

class ChangePrivilegesTC(InvestigationEditingTC):
    # zmiana uprawnień
    def runTest(self):
        core.set_privileges('S101', 'P100', 'odczyt/zapis')
        cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P100'")
        self.assertEqual(cur.rowcount, 1)
        (privileges,) = cur.fetchone()
        self.assertEqual(privileges, 'odczyt/zapis')

class GivePrivilegesTC(InvestigationEditingTC):        
    # dodanie uprawnień do sprawy nowemu użytkownikowi
    def runTest(self):
        core.set_privileges('S101', 'P105', 'odczyt')
        cur.execute("SELECT Uprawnienia FROM uprawnienia WHERE Sprawa='S101' AND Policjant='P105'")
        self.assertEqual(cur.rowcount, 1)
        (privileges,) = cur.fetchone()
        self.assertEqual(privileges, 'odczyt')



# suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
# unittest.TextTestRunner(verbosity=2).run(suite)
