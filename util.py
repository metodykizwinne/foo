# -*- coding: utf-8 -*-

HOST='metodyki.dyndns.org'
# HOST='localhost'
DBNAME='pgdatabase'
USER='pguser'
PASSWORD='tylkosystemlinux'
TESTDBNAME='test'
TESTUSER=USER
TESTPASSWORD=PASSWORD

import psycopg2

def insert_privileges(dbconn, record):
    cur = dbconn.cursor()
    cur.execute("INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES (%s, %s, %s)", record)
    
def insert_investigation(dbconn, record):    
    cur = dbconn.cursor()
    cur.execute("INSERT INTO sprawy (Sprawa, Policjant, Data_otwarcia, Data_zamkniecia) VALUES (%s, %s, %s, %s)", record)

def insert_user(dbconn, record):    
    cur = dbconn.cursor()
    cur.execute("INSERT INTO uzytkownicy (Policjant, Imie, Nazwisko) VALUES (%s, %s, %s)", record)



    
