# -*- coding: utf-8 -*-

import psycopg2
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect("port=5432 host=metodyki.dynds.org dbname=test user=pguser password='tylkosystemlinux'")
        self.cur = conn.cursor()
        self.cur.execute("INSERTO INTO uprawnienia ('P100','S100','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P101','S100','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P102','S100','odczyt/zapis');")
        self.cur.execute("INSERTO INTO uprawnienia ('P103','S100','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P104','S100','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P100','S101','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P101','S101','odczyt/zapis');")
        self.cur.execute("INSERTO INTO uprawnienia ('P102','S100','odczyt');")
        self.cur.execute("INSERTO INTO uprawnienia ('P105','S100','odczyt');")
        self.scur.execute("INSERTO INTO uprawnienia ('P100','S102','odczyt/zapis');")

    def test_set_privileges(self):
        with self.assertRaises(NoSuchCaseError):
            set_privileges('S105','P100','odczyt')
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

    def tearDown(self):
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik = 'P100' AND sprawa='S100' AND typ= 'odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P101' AND sprawa='S100' AND typ='odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P102' AND sprawa='S100' AND typ='odczyt/zapis');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P103' AND sprawa='S100' AND typ='odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P104' AND sprawa='S100' AND typ='odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P100' AND sprawa='S101' AND typ='odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P101' AND sprawa='S101' AND typ='odczyt/zapis');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P102' AND sprawa='S100' AND typ='odczyt');")
        self.cur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P105' AND sprawa='S100' AND typ='odczyt');")
        self.scur.execute("DELETE FROM uprawnienia WHERE uzytkownik ='P100' AND sprawa='S102' AND typ='odczyt/zapis');")

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
