# -*- coding: utf-8 -*-

import psycopg2

def insert_privileges(cursor, record):
    cursor.execute("INSERT INTO uprawnienia (Sprawa, Policjant, Uprawnienia) VALUES (%s, %s, %s)", record)
    
    
