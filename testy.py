# -*- coding: utf-8 -*-

import psycopg2
import unittest

class TestInvestigationEditing(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect("port=5432 host=metodyki.dynds.org dbname=test user=pguser password='tylkosystemlinux'")
        self.cur = conn.cursor()
        self.cur.execute("CREATE TABLE uprawnienia ( U_Id int, Policjant varchar(255), Sprawa varchar(255), Uprawnienia varchar(255) );" + \
        "INSERT INTO uprawnienia ('P100','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P101','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P102','S100','odczyt/zapis');" + \
        "INSERT INTO uprawnienia ('P103','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P104','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P100','S101','odczyt');" + \
        "INSERT INTO uprawnienia ('P101','S101','odczyt/zapis');" + \
        "INSERT INTO uprawnienia ('P102','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P105','S100','odczyt');" + \
        "INSERT INTO uprawnienia ('P100','S102','odczyt/zapis');")

    def test_set_privileges(self):
        with self.assertRaises(NoSuchCaseError):
            set_privileges('S105','P100','odczyt')

        with self.assertRaises(NoSuchUserError):
            set_privileges('S100', 'P106', 'odczyt/zapis')
# powinna być jeszcze przynajmniej zmiana uprawnień i usunięcie rekordu poprzez ich odebranie
# + opcjonalnie można potem sprawdzać całą tabelę albo przynajmniej czy liczba rekordów się zgadza


    def tearDown(self):
        self.cur.execute("DROP TABLE uprawnienia;")

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
