# -*- coding: utf-8 -*-

HOST='metodyki.dyndns.org'
DBNAME='pgdatabase'
TESTDBNAME='test'
TESTUSER='pguser'
TESTPASSWORD='tylkosystemlinux'

import psycopg2

def insert_privileges(cursor, record):
    cursor.execute("INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES (%s, %s, %s)", record)
    
    
