# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:25:07 2016

@author: csx
"""
import json
import sqlite3

conn = sqlite3.connect("rosterDB.sqlite")
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
name TEXT UNIQUE,
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);

CREATE TABLE Course(
title TEXT UNIQUE,
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);

CREATE TABLE Member(
user_id INTEGER,
course_id INTEGER,
role INTEGER,
PRIMARY KEY (user_id, course_id));
''')

#fh = open("roster_data.json")
data = json.load(open("roster_data.json")) # a list

for entry in data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('''INSERT OR IGNORE INTO User (name) 
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) 
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ? ,?)''', 
        ( user_id, course_id, role) )

conn.commit()
